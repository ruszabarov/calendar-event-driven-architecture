# publisher.py
import pika
import json
import uuid

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# Declare queues
channel.queue_declare(queue='meeting_queue')
channel.queue_declare(queue='participant_queue')
channel.queue_declare(queue='attachment_queue')
channel.queue_declare(queue='response_queue')

# Callback function for response handling
def on_response(ch, method, properties, body):
    response_data = json.loads(body)
    print("Received response:", response_data)

    if response_data['type'] == 'participant':
        update_meeting_with_participant(response_data['meeting_id'], response_data['participant_id'])
    elif response_data['type'] == 'attachment':
        update_meeting_with_attachment(response_data['meeting_id'], response_data['attachment_id'])

def update_meeting_with_participant(meeting_id, participant_id):
    update_data = {
        "command": "update",
        "meetingId": meeting_id,
        "participantId": participant_id
    }
    channel.basic_publish(exchange='', routing_key='meeting_queue', body=json.dumps(update_data))
    print("Published participant update to meeting broker:", update_data)

def update_meeting_with_attachment(meeting_id, attachment_id):
    update_data = {
        "command": "update",
        "meetingId": meeting_id,
        "attachmentId": attachment_id
    }
    channel.basic_publish(exchange='', routing_key='meeting_queue', body=json.dumps(update_data))
    print("Published attachment update to meeting broker:", update_data)

# Set up a consumer to listen for responses
channel.basic_consume(queue='response_queue', on_message_callback=on_response, auto_ack=True)

# Start the consumer
print('Waiting for responses. To exit press CTRL+C')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Exiting...")
    channel.stop_consuming()
finally:
    connection.close()

