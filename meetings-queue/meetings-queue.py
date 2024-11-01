import pika
import json
import requests
import os
import threading

# RabbitMQ host
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE1_NAME = "meeting_queue"
QUEUE2_NAME = "response_queue"
DLQ1_NAME = "meeting_queue_dlq"
DLQ2_NAME = "response_queue_dlq"

# Endpoint URLs
ENDPOINT_URL = "http://krakend:8080/meetings"
ENDPOINT_URL2 = (
    "http://krakend:8080/meetings/{meetingId}/addParticipant/{participantId}"
)
ENDPOINT_URL3 = "http://krakend:8080/meetings/{meetingId}/addAttachment/{attachmentId}"


# Callback function for consuming messages from meeting_queue
def on_message1(ch, method, properties, body):
    try:
        # Parse message body
        message = json.loads(body)
        print(f"Received message from {QUEUE1_NAME}: {message}")

        # Extract only necessary meeting information
        meeting_data = {
            "id": message.get("id"),
            "title": message.get("title"),
            "location": message.get("location"),
            "datetime": message.get("datetime"),
        }

        # Make a POST request to the specified endpoint with stripped-down meeting data
        response = requests.post(ENDPOINT_URL, json=meeting_data)

        # Log response from the endpoint
        if response.status_code == 200:
            print(f"Successfully processed message from {QUEUE1_NAME}: {meeting_data}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            raise Exception(f"Failed with status code: {response.status_code}")

    except Exception as e:
        print(f"Error processing message from {QUEUE1_NAME}: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        ch.basic_publish(exchange="", routing_key=DLQ1_NAME, body=body)


# Callback function for consuming messages from response_queue


def on_message2(ch, method, properties, body):
    try:
        # Parse message body
        message = json.loads(body)
        meeting_id = message["meetingId"]
        print(f"Received message from {QUEUE2_NAME}: {message}")

        # Determine which scenario to use based on presence of "url" field
        if "url" in message:
            # Scenario 2: Process with ENDPOINT_URL3
            attachment_id = message[
                "id"
            ]  # Assuming "id" is used for attachment in this context
            url = ENDPOINT_URL3.format(meetingId=meeting_id, attachmentId=attachment_id)
            print("Processing with ENDPOINT_URL3")
        else:
            # Scenario 1: Process with ENDPOINT_URL2
            participant_id = message["id"]
            url = ENDPOINT_URL2.format(
                meetingId=meeting_id, participantId=participant_id
            )
            print("Processing with ENDPOINT_URL2")

        # Make a GET request to the specified endpoint with message data
        response = requests.get(url, json=message)

        # Log response from the endpoint
        if response.status_code == 200:
            print(f"Successfully processed message from {QUEUE2_NAME}: {message}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            raise Exception(f"Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error processing message from {QUEUE2_NAME}: {e}")

        # Send to DLQ after exceeding retry count
        print(f"Message sent to {DLQ2_NAME}: {message}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        ch.basic_publish(exchange="", routing_key=DLQ2_NAME, body=body)


# Set up consumer for each queue in separate threads with separate connections
def start_consumer1():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(
        queue=QUEUE1_NAME,
    )
    channel.queue_declare(queue=DLQ1_NAME)
    channel.basic_consume(queue=QUEUE1_NAME, on_message_callback=on_message1)
    print(f"Waiting for messages in {QUEUE1_NAME}. To exit, press CTRL+C")
    channel.start_consuming()


def start_consumer2():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(
        queue=QUEUE2_NAME,
    )
    channel.queue_declare(queue=DLQ2_NAME)
    channel.basic_consume(queue=QUEUE2_NAME, on_message_callback=on_message2)
    print(f"Waiting for messages in {QUEUE2_NAME}. To exit, press CTRL+C")
    channel.start_consuming()


# Start each consumer in a separate thread
threading.Thread(target=start_consumer1).start()
threading.Thread(target=start_consumer2).start()
