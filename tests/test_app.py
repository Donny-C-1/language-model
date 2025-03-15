# tests/test_app.py
import pytest
from app import app  # Assuming your Flask app is in app.py
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_default_endpoint(client):
    response = client.get('/', json={'question': 'What is your name?'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'message' in data
    # Add more assertions to check the answer

#Add more test for all of your endpoints, and all of your functions.