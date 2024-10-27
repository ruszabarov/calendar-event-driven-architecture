# UNIT TESTS FOR PARTICIPANTS SERVICE THROUGH API GATEWAY

import unittest
import requests
import json

KRANKEND_API_URL = "http://localhost:8080"

class TestParticipantsMicroservice(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.participant_url = f"{KRANKEND_API_URL}/participants"
        cls.sample_participant = {
            "name": "John Doe",
            "email": "johndoe@example.com"
        }
        headers = {'Content-Type': 'application/json'}
        
        # Create the participant
        response = requests.post(cls.participant_url, data=json.dumps(cls.sample_participant), headers=headers)
        if response.status_code in [200, 201]:
            res = requests.get(cls.participant_url).json()
            cls.sample_participant['id'] = res['data'][0]['id']
        else:
            raise Exception("Failed to create participant in setup")

    def test_get_all_participants(self):
        response = requests.get(self.participant_url)
        self.assertIn(response.status_code, [200, 201])
        res = response.json()
        participants = res['data']
        self.assertIsInstance(participants, list)

    def test_get_single_participant(self):
        url = f"{self.participant_url}/{self.sample_participant['id']}"
        response = requests.get(url)
        self.assertIn(response.status_code, [200, 202])
        participant = response.json()['data']
        self.assertEqual(participant['name'], self.sample_participant['name'])

    def test_update_participant(self):
        updated_data = {"name": "John Doe Updated", "email": "johnupdated@example.com"}
        url = f"{self.participant_url}/{self.sample_participant['id']}"
        headers = {'Content-Type': 'application/json'}
        response = requests.put(url, data=json.dumps(updated_data), headers=headers)
        self.assertIn(response.status_code, [200, 204])
        updated_participant = response.json()
        self.assertEqual(updated_participant['name'], "John Doe Updated")

    def test_delete_participant(self):
        url = f"{self.participant_url}/{self.sample_participant['id']}"
        response = requests.delete(url)
        self.assertIn(response.status_code, [200, 204])
        get_response = requests.get(url)
        self.assertIn(get_response.status_code, [500, 404, 410])

# Force the delete test to run last
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestParticipantsMicroservice('test_get_all_participants'))
    suite.addTest(TestParticipantsMicroservice('test_get_single_participant'))
    suite.addTest(TestParticipantsMicroservice('test_update_participant'))
    suite.addTest(TestParticipantsMicroservice('test_delete_participant'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
