# consumer.py
import pika
import json
import requests
import os

# RabbitMQ host
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
QUEUE_NAME = 'attachment_queue'
RESPONSE_QUEUE_NAME = 'response_queue'

# Endpoint URL (Set this as an environment variable in your container)
ENDPOINT_URL = 'http://krakend:8080/attachments'

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Ensure the queue is declared in the consumer as well
channel.queue_declare(queue=QUEUE_NAME)
channel.queue_declare(queue=RESPONSE_QUEUE_NAME)

# Callback function for consuming messages
def on_message(ch, method, properties, body):
    try:
        # Parse message body
        message = json.loads(body)
        print(f"Received message: {message}")

        # Make a POST request to the specified endpoint with message data
        response = requests.post(ENDPOINT_URL, json=message)
        
        # Log response from the endpoint
        if response.status_code == 200:
            print(f"Successfully processed message: {message}")
            # Publish the same message to the response queue
            channel.basic_publish(exchange='', routing_key=RESPONSE_QUEUE_NAME, body=json.dumps(message))
        else:
            print(f"Failed to process message: {message} - Status code: {response.status_code}")
    
    except Exception as e:
        print(f"Error processing message: {e}")

    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up consumer on participant_queue
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)

print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
