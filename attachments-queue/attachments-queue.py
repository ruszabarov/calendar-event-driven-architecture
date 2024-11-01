import pika
import json
import requests
import os

# RabbitMQ host
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "attachment_queue"
RESPONSE_QUEUE_NAME = "response_queue"
DLQ_ATTACHMENT_QUEUE_NAME = "attachment_queue_dlq"

# Endpoint URL
ENDPOINT_URL = "http://krakend:8080/attachments"
MAX_RETRIES = 0  # Maximum number of retry attempts

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Ensure queues are declared with DLQ for response queue
channel.queue_declare(queue=QUEUE_NAME)
channel.queue_declare(
    queue=RESPONSE_QUEUE_NAME,
)
channel.queue_declare(queue=DLQ_ATTACHMENT_QUEUE_NAME)


def on_message(ch, method, properties, body):
    try:
        # Parse message body
        message = json.loads(body)
        print(f"Received message: {message}")

        # Extract only necessary attachment information
        attachment_data = {
            "id": message.get("id"),
            "url": message.get("url"),
        }

        # Make a POST request to the specified endpoint with stripped-down attachment data
        response = requests.post(ENDPOINT_URL, json=attachment_data)

        # Log response and publish to response queue if successful
        if response.status_code == 200:
            print(f"Successfully processed message: {attachment_data}")

            # Include the meetingId in the response data if required
            response_data = response.json()
            response_data["meetingId"] = message.get("meetingId")

            # Publish the modified response with meetingId to the response queue
            ch.basic_publish(
                exchange="",
                routing_key=RESPONSE_QUEUE_NAME,
                body=json.dumps(response_data),
            )
            print(f"Published message to response queue: {response_data}")
        else:
            raise Exception(f"Failed with status code: {response.status_code}")

    except Exception as e:
        print(f"Error processing message: {e}")
        #ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        ch.basic_publish(exchange="", routing_key=DLQ_ATTACHMENT_QUEUE_NAME, body=body)

    # Acknowledge message if successful
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Set up consumer on participant_queue
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)

print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
