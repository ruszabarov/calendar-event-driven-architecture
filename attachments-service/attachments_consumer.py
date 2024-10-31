import pika
import json
import sys
import uuid
import os
from urllib.parse import urlparse

# RabbitMQ host
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
ATTACHMENT_QUEUE = 'attachment_queue'
RESPONSE_QUEUE = 'response_queue'
DLQ_RESPONSE_QUEUE = 'response_queue_dlq'

MAX_RETRIES = 3

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=ATTACHMENT_QUEUE)

channel.queue_declare(
    queue=RESPONSE_QUEUE,
    arguments={
        'x-dead-letter-exchange': '',
        'x-dead-letter-routing-key': DLQ_RESPONSE_QUEUE,
    }
)
channel.queue_declare(queue=DLQ_RESPONSE_QUEUE)


def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https')


def process_message(ch, method, properties, body):
    try:
        # Parse message body
        message = json.loads(body)
        print(f"Received message: {message}")

        command = message.get('command')

        if command == 'create':
            attachment_id = message.get('id') or str(uuid.uuid4())
            meeting_id = message.get('meetingId')
            url = message.get('url')

            # Validate URL
            if not url or not is_valid_url(url):
                raise ValueError("Invalid URL format")

            print(f"Attachment {attachment_id} processed successfully.")

            response = {
                'type': 'attachment',
                'status': 'success',
                'attachment_id': attachment_id,
                'meetingId': meeting_id,
                'message': 'Attachment processed successfully'
            }

            ch.basic_publish(
                exchange='',
                routing_key=RESPONSE_QUEUE,
                body=json.dumps(response),
                properties=pika.BasicProperties()
            )
            print(f"Published message to response queue: {response}")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            raise ValueError(f"Unknown command: {command}")

    except Exception as e:
        print(f"Error processing message: {e}")

        retries = properties.headers.get("x-retries", 0) if properties.headers else 0

        if retries < MAX_RETRIES:
            headers = properties.headers or {}
            headers["x-retries"] = retries + 1
            print(f"Retrying message: {message}, attempt {retries + 1}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.basic_publish(
                exchange="",
                routing_key=ATTACHMENT_QUEUE,
                body=body,
                properties=pika.BasicProperties(headers=headers),
            )
        else:
            print(
                f"Message sent to {DLQ_RESPONSE_QUEUE} after {MAX_RETRIES} retries: {message}"
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.basic_publish(
                exchange="",
                routing_key=DLQ_RESPONSE_QUEUE,
                body=body
            )


channel.basic_consume(queue=ATTACHMENT_QUEUE, on_message_callback=process_message)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
