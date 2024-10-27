from flask import Flask, request, jsonify
from db import init_db
from models import Participant
import uuid
import re

app = Flask(__name__)

@app.before_first_request
def initialize():
    init_db()

# Helper function for email validation
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

@app.route('/participants', methods=['GET'])
def get_participants():
    ids = request.args.get('ids')
    if ids:
        participant_ids = ids.split(',')
        participants = Participant.get_multiple(participant_ids)
        return jsonify([p.to_dict() for p in participants if p is not None]), 200
    else:
        participants = Participant.get_all()
        return jsonify([p.to_dict() for p in participants]), 200


@app.route('/participants/<participant_id>', methods=['GET'])
def get_participant(participant_id):
    participant = Participant.get(participant_id)
    if participant:
        return jsonify(participant.to_dict()), 200
    return jsonify({"error": "Participant not found"}), 404


@app.route('/participants', methods=['POST'])
def create_participant():
    data = request.get_json()

    # Validate input data
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400

    if len(data['name']) > 600:
        return jsonify({"error": "Name must not exceed 600 characters"}), 400

    if not is_valid_email(data['email']):
        return jsonify({"error": "Invalid email format"}), 400

    participant_id = data.get('id', str(uuid.uuid4()))  # Generate a UUID if not provided
    participant = Participant.create(participant_id, data['name'], data['email'])
    
    if participant:
        return jsonify(participant.to_dict()), 200
    return jsonify({"error": "Could not create participant"}), 400


@app.route('/participants/<participant_id>', methods=['PUT'])
def update_participant(participant_id):
    data = request.get_json()
    
    # Validate input data
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400

    if len(data['name']) > 600:
        return jsonify({"error": "Name must not exceed 600 characters"}), 400

    if not is_valid_email(data['email']):
        return jsonify({"error": "Invalid email format"}), 400

    participant = Participant.update(participant_id, data['name'], data['email'])
    if participant:
        return jsonify(participant.to_dict()), 200
    return jsonify({"error": "Participant not found"}), 404


@app.route('/participants/<participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    success = Participant.delete(participant_id)
    if success:
        return jsonify({"message": "Participant deleted"}), 200
    return jsonify({"error": "Participant not found"}), 404


if __name__ == '__main__':
    init_db()  # Initialize the database when running the script directly
    app.run(host='0.0.0.0', port=8080, debug=True)
