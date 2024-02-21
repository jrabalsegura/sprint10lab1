import pytest
from flask import json
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
os.environ['FLASK_ENV'] = 'testing'
from app import create_app, db


@pytest.fixture
def client():
    env_name = os.getenv("FLASK_ENV", "testing")
    app = create_app(env_name)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_insert_data(client):
    """Test inserting new data."""
    response = client.post('/data', json={'name': 'Test Data'})
    assert response.status_code == 200
    assert b'Data inserted successfully' in response.data

def test_get_all_data(client):
    """Test retrieving all data."""
    # Insert data for testing retrieval
    client.post('/data', json={'name': 'Test Data'})

    response = client.get('/data')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Test Data'

def test_delete_data(client):
    """Test deleting data."""
    name = 'Test Data'
    client.post('/data', json={'name': name})
    
    get_response = client.get('/data')
    data = json.loads(get_response.data)
    
    # Encuentra el objeto con el 'name' que has insertado y obtén su 'id'.
    data_item = next((item for item in data if item['name'] == name), None)
    assert data_item is not None, "Data item was not found."
    data_id = data_item['id']
    
    # Probamos endpoint DELETE
    del_response = client.delete(f'/data/{data_id}')
    assert del_response.status_code == 200
    assert b'Data deleted successfully' in del_response.data


