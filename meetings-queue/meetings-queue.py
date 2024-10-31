import pika
import json
import requests
import os
import threading

# RabbitMQ host
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
QUEUE1_NAME = 'meeting_queue'
QUEUE2_NAME = 'response_queue'

# Endpoint URLs
ENDPOINT_URL = 'http://krakend:8080/meetings'
ENDPOINT_URL2 = 'http://krakend:8080//meetings/{meetingId}/addParticipant/{participantId}'

# Ensure each consumer gets its own connection and channel

# Callback function for consuming messages from meeting_queue
def on_message1(ch, method, properties, body):
    try:
        # Parse message body
        message = json.loads(body)
        print(f"Received message from {QUEUE1_NAME}: {message}")

        # Make a POST request to the specified endpoint with message data
        response = requests.post(ENDPOINT_URL, json=message)
        
        # Log response from the endpoint
        if response.status_code == 200:
            print(f"Successfully processed message from {QUEUE1_NAME}: {message}")
        else:
            print(f"Failed to process message from {QUEUE1_NAME}: {message} - Status code: {response.status_code}")
    
    except Exception as e:
        print(f"Error processing message from {QUEUE1_NAME}: {e}")

    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Callback function for consuming messages from response_queue
def on_message2(ch, method, properties, body):
    try:
        # Parse message body
        message = json.loads(body)
        participant_id = message['id']
        meeting_id = message['meetingId']
        url = ENDPOINT_URL2.format(meetingId=meeting_id, participantId=participant_id)

        print(f"Received message from {QUEUE2_NAME}: {message}")

        # Make a POST request to the specified endpoint with message data
        response = requests.post(url, json=message)
        
        # Log response from the endpoint
        if response.status_code == 200:
            print(f"Successfully processed message from {QUEUE2_NAME}: {message}")
        else:
            print(f"Failed to process message from {QUEUE2_NAME}: {message} - Status code: {response.status_code}")
    
    except Exception as e:
        print(f"Error processing message from {QUEUE2_NAME}: {e}")

    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up consumer for each queue in separate threads with separate connections
def start_consumer1():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE1_NAME)
    channel.basic_consume(queue=QUEUE1_NAME, on_message_callback=on_message1)
    print(f'Waiting for messages in {QUEUE1_NAME}. To exit, press CTRL+C')
    channel.start_consuming()

def start_consumer2():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE2_NAME)
    channel.basic_consume(queue=QUEUE2_NAME, on_message_callback=on_message2)
    print(f'Waiting for messages in {QUEUE2_NAME}. To exit, press CTRL+C')
    channel.start_consuming()

# Start each consumer in a separate thread
threading.Thread(target=start_consumer1).start()
threading.Thread(target=start_consumer2).start()
