import sqlite3
import uuid
from db import get_db

class Participant:
    @staticmethod
    def get_all():
        conn = get_db()
        cur = conn.execute('SELECT * FROM participants')
        rows = cur.fetchall()
        return [Participant.from_row(row) for row in rows]

    @staticmethod
    def get(participant_id):
        conn = get_db()
        cur = conn.execute('SELECT * FROM participants WHERE id = ?', (participant_id,))
        row = cur.fetchone()
        return Participant.from_row(row) if row else None

    @staticmethod
    def get_multiple(participant_ids):
        participants = []
        for participant_id in participant_ids:
            participant = Participant.get(participant_id)
            if participant:
                participants.append(participant)
        return participants

    @staticmethod
    def create(participant_id, name, email):
        conn = get_db()
        with conn:
            cur = conn.execute(
                'INSERT INTO participants (id, name, email) VALUES (?, ?, ?)', 
                (participant_id, name, email)
            )
            # Fetch the newly added participant
            row = conn.execute(
                'SELECT id, name, email FROM participants WHERE id = ?', 
                (participant_id,)
            ).fetchone()
            return Participant.from_row(row) if row else None



    @staticmethod
    def update(participant_id, name, email):
        conn = get_db()
        with conn:
            conn.execute('UPDATE participants SET name = ?, email = ? WHERE id = ?', (name, email, participant_id))
        return Participant.get(participant_id)

    @staticmethod
    def delete(participant_id):
        conn = get_db()
        with conn:
            cur = conn.execute('DELETE FROM participants WHERE id = ?', (participant_id,))
            return cur.rowcount > 0

    @staticmethod
    def from_row(row):
        return Participant(row['id'], row['name'], row['email'])

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}
