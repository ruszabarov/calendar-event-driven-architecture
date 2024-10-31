import pika
import json
import requests
import os

# RabbitMQ host
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "participant_queue"
RESPONSE_QUEUE_NAME = "response_queue"
DLQ_RESPONSE_QUEUE_NAME = "response_queue_dlq"

# Endpoint URL
ENDPOINT_URL = "http://krakend:8080/participants"
MAX_RETRIES = 3  # Maximum number of retry attempts

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Ensure queues are declared with DLQ for response queue
channel.queue_declare(queue=QUEUE_NAME)
channel.queue_declare(
    queue=RESPONSE_QUEUE_NAME,
    arguments={
        "x-dead-letter-exchange": "",
        "x-dead-letter-routing-key": DLQ_RESPONSE_QUEUE_NAME,
    },
)
channel.queue_declare(queue=DLQ_RESPONSE_QUEUE_NAME)


# Callback function for consuming messages from participant_queue
def on_message(ch, method, properties, body):
    try:
        # Parse message body
        message = json.loads(body)
        print(f"Received message: {message}")

        # Make a POST request to the specified endpoint with message data
        response = requests.post(ENDPOINT_URL, json=message)

        # Log response and publish to response queue if successful
        if response.status_code == 200:
            print(f"Successfully processed message: {message}")
            headers = properties.headers or {}
            headers["x-retries"] = headers.get("x-retries", 0)  # Start with 0 retries

            # Publish the message to the response queue with headers
            channel.basic_publish(
                exchange="",
                routing_key=RESPONSE_QUEUE_NAME,
                body=json.dumps(message),
                properties=pika.BasicProperties(headers=headers),
            )
            print(f"Published message to response queue: {message}")
        else:
            raise Exception(f"Failed with status code: {response.status_code}")

    except Exception as e:
        print(f"Error processing message: {e}")

        # Get current retry count from headers
        retries = properties.headers.get("x-retries", 0) if properties.headers else 0

        if retries < MAX_RETRIES:
            # Increment retry count and requeue message with updated headers
            headers = properties.headers or {}
            headers["x-retries"] = retries + 1
            print(f"Retrying message: {message}, attempt {retries + 1}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=body,
                properties=pika.BasicProperties(headers=headers),
            )
        else:
            # Send to DLQ after exceeding retry count
            print(
                f"Message sent to {DLQ_RESPONSE_QUEUE_NAME} after {MAX_RETRIES} retries: {message}"
            )
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            channel.basic_publish(
                exchange="", routing_key=DLQ_RESPONSE_QUEUE_NAME, body=body
            )

    # Acknowledge message if successful
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Set up consumer on participant_queue
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)

print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
