import pika
import json
import requests
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "attachment_queue"
RESPONSE_QUEUE_NAME = "attachment_response_queue"
DLQ_RESPONSE_QUEUE_NAME = "attachment_response_dlq"

ENDPOINT_URL = "http://krakend:8080/attachments"
MAX_RETRIES = 3

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)
channel.queue_declare(
    queue=RESPONSE_QUEUE_NAME,
    arguments={
        "x-dead-letter-exchange": "",
        "x-dead-letter-routing-key": DLQ_RESPONSE_QUEUE_NAME,
    },
)
channel.queue_declare(queue=DLQ_RESPONSE_QUEUE_NAME)

def on_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        print(f"Received message: {message}")
        response = requests.post(ENDPOINT_URL, json=message)
        if response.status_code == 200:
            print(f"Successfully processed message: {message}")
            headers = properties.headers or {}
            headers["x-retries"] = headers.get("x-retries", 0)
            response_data = response.json()
            response_data["meetingId"] = message.get("meetingId")
            ch.basic_publish(
                exchange="",
                routing_key=RESPONSE_QUEUE_NAME,
                body=json.dumps(response_data),
                properties=pika.BasicProperties(headers=headers),
            )
            print(f"Published message to response queue: {response_data}")
        else:
            raise Exception(f"Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error processing message: {e}")
        retries = properties.headers.get("x-retries", 0) if properties.headers else 0
        if retries < MAX_RETRIES:
            headers = properties.headers or {}
            headers["x-retries"] = retries + 1
            print(f"Retrying message: {message}, attempt {retries + 1}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            ch.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=body,
                properties=pika.BasicProperties(headers=headers),
            )
        else:
            print(f"Message sent to {DLQ_RESPONSE_QUEUE_NAME} after {MAX_RETRIES} retries: {message}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            ch.basic_publish(
                exchange="",
                routing_key=DLQ_RESPONSE_QUEUE_NAME,
                body=body
            )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)

print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
