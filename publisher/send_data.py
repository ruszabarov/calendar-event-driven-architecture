# send_test_messages.py
import pika
import json
import os

# RabbitMQ host
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Declare queues with DLQ configurations matching the consumers

# Meeting queue and its DLQ
channel.queue_declare(
    queue="meeting_queue",
    arguments={
        "x-dead-letter-exchange": "",
        "x-dead-letter-routing-key": "meeting_queue_dlq",
    },
)
channel.queue_declare(queue="meeting_queue_dlq")

# Participant queue and response queue with DLQ configurations
channel.queue_declare(queue="participant_queue")
channel.queue_declare(
    queue="response_queue",
    arguments={
        "x-dead-letter-exchange": "",
        "x-dead-letter-routing-key": "response_queue_dlq",
    },
)
channel.queue_declare(queue="response_queue_dlq")

# Attachment queue
channel.queue_declare(queue="attachment_queue")
# The attachment_queue consumer also publishes to response_queue


# Function to publish a create meeting message
def create_meeting(meeting_data):
    meeting_data["command"] = "create"
    channel.basic_publish(
        exchange="", routing_key="meeting_queue", body=json.dumps(meeting_data)
    )
    print("Published create meeting message:", meeting_data)


# Function to publish a create participant message
def create_participant(participant_data):
    participant_data["command"] = "create"
    channel.basic_publish(
        exchange="", routing_key="participant_queue", body=json.dumps(participant_data)
    )
    print("Published create participant message:", participant_data)


# Function to publish a create attachment message
def create_attachment(attachment_data):
    attachment_data["command"] = "create"
    channel.basic_publish(
        exchange="", routing_key="attachment_queue", body=json.dumps(attachment_data)
    )
    print("Published create attachment message:", attachment_data)


# Main function to load data from JSON and send creation messages
def load_and_publish_data(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

            # Parse and publish each type of data
            for meeting in data.get("meetings", []):
                create_meeting(meeting)
            for participant in data.get("participants", []):
                create_participant(participant)
            for attachment in data.get("attachments", []):
                create_attachment(attachment)

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in file {file_path}: {e}")


if __name__ == "__main__":
    load_and_publish_data("test_data.json")
