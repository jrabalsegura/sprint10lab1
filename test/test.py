import pytest
from flask import json
from app import create_app, db


@pytest.fixture
def client():
    app = create_app('testing')
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
    post_response = client.post('/data', json={'name': 'Test Data'})
    post_data = json.loads(post_response.data)
    data_id = post_data['id']

    del_response = client.delete(f'/data/{data_id}')
    assert del_response.status_code == 200
    assert b'Data deleted successfully' in del_response.data
