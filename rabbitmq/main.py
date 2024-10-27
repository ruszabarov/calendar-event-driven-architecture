#!/usr/bin/env python
import pika
import json


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="attachments_and_participants", durable=True)
channel.queue_declare(queue="meetings", durable=True)

print("Queues created successfully")


def publish_meetings_batch(meetings_batch):
    for meeting in meetings_batch:
        message = json.dumps(meeting)

        channel.basic_publish(
            exchange="",
            routing_key="attachments_and_participants",
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

        print("Batch of meetings published to the queue")


def attachments_and_participants_callback(ch, method, properties, body):
    meeting = json.load(body)
    print(f"Processing attachments for meeting: {meeting['id']}")

    # TODO: Create attachments here

    # TODO: Create participants here

    # TODO: Adjust the message to include the new ids

    channel.basic_publish(
        exchange="",
        routing_key="meetings",
        body=json.dumps(meeting),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )


channel.basic_consume(
    queue="attachments_and_participants",
    on_message_callback=attachments_and_participants_callback,
)


def meetings_callback(ch, method, properties, body):
    meeting = json.loads(body)

    # TODO: Create meetings here

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue="meetings", on_message_callback=meetings_callback)

channel.start_consuming()
