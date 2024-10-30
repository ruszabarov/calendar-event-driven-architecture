import os
import pika
import requests
import json

# Environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "commands_queue")

# Microservice endpoint URLs
MICROSERVICE_CREATE_URL = "http://localhost:5000/create"
MICROSERVICE_ADD_PARTICIPANT_URL_TEMPLATE = (
    "http://krakend:3000/meetings/{meetingId}/addParticipant/{participantId}"
)

MICROSERVICE_ADD_ATTACHMENT_URL_TEMPLATE = (
    "http://krakend:3000/meetings/{meetingId}/addAttachment/{attachmentId}"
)


def process_message(ch, method, properties, body):
    print(f"Received message: {body}")

    # Parse the JSON message
    try:
        message = json.loads(body)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Determine the command type
    command_type = message.get("command")
    if command_type == "create":
        url = MICROSERVICE_CREATE_URL

        try:
            response = requests.post(url, json=message)
            response.raise_for_status()
            print("Successfully processed create command")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to microservice: {e}")
    elif command_type == "update":
        # Extract the required parameters for the update URL
        meeting_id = message.get("meetingId")
        participant_id = message.get("participantId")
        attachment_id = message.get("attachmentId")

        # Check if both parameters are provided
        if not meeting_id:
            print("Missing 'meetingId' in update message.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if not participant_id and not attachment_id:
            print("Missing either 'participantId' or 'attachmentId' in update message")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        url = ""

        if participant_id:
            # Construct the update URL with parameters
            url = MICROSERVICE_ADD_PARTICIPANT_URL_TEMPLATE.format(
                meetingId=meeting_id, participantId=participant_id
            )
        elif attachment_id:
            url = MICROSERVICE_ADD_ATTACHMENT_URL_TEMPLATE.format(
                meetingId=meeting_id, participantId=participant_id
            )

        try:
            response = requests.get(url, json=message)
            response.raise_for_status()
            print("Successfully processed update command")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to microservice: {e}")

    else:
        print(f"Unknown command: {command_type}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    # Start consuming messages
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=process_message)

    print("Waiting for messages. To exit, press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Exiting...")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
