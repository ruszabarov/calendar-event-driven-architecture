import pika
import json
import uuid

rabbitmq_host = 'localhost'  # Ensure this points to your RabbitMQ server

def publish_message(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host)
    )
    channel = connection.channel()

    queue_name = 'attachments_queue'
    # Remove the queue_declare line
    # channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )
    print("Sent message")
    connection.close()

if __name__ == '__main__':
    attachment_message = {
        'attachment': {
            'id': str(uuid.uuid4()),
            'meeting_id': str(uuid.uuid4()),
            'url': 'http://example.com/file.pdf'
        }
    }
    publish_message(attachment_message)
