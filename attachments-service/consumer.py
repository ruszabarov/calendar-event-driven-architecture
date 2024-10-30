import uuid

import pika
import json
import sys
from urllib.parse import urlparse

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import schemas
import models

models.Base.metadata.create_all(bind=engine)
rabbitmq_host = 'localhost'  # Use the hostname/IP address of  RabbitMQ server


def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https')


def process_message(ch, method, properties, body):
    db: Session = SessionLocal()
    try:
        message = json.loads(body)
        attachment_data = message.get('attachment')

        # Validating data
        if not attachment_data:
            raise ValueError("No attachment data in message")

        attachment_id = attachment_data.get('id') or str(uuid.uuid4())
        meeting_id = attachment_data.get('meeting_id')
        url = attachment_data.get('url')

        # Validating URL
        if not is_valid_url(url):
            raise ValueError("Invalid URL format")

        # Creating Attachment object
        new_attachment = schemas.AttachmentCreate(
            id=attachment_id,
            meeting_id=meeting_id,
            url=url
        )

        # Saving to database
        crud.create_attachment(db, new_attachment)
        print(f"Attachment {attachment_id} processed successfully.")

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Failed to process message: {e}")
        # Reject the message and requeue it or send to dead-letter queue
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    finally:
        db.close()


def consume_messages():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host)
    )
    channel = connection.channel()

    queue_name = 'attachments_queue'
    channel.queue_declare(
        queue=queue_name,
        durable=True,
        arguments={
            'x-dead-letter-exchange': '',
            'x-dead-letter-routing-key': 'attachments_dead_letter_queue'
        }
    )

    channel.queue_declare(queue='attachments_dead_letter_queue', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=process_message
    )

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        consume_messages()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
