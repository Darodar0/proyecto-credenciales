import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Acceso de Usuario' in response.data

def test_successful_authentication(client):
    response = client.post('/auth', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'

def test_failed_authentication_missing_data(client):
    response = client.post('/auth', data={
        'email': 'test@example.com'
    })
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['status'] == 'error'

def test_failed_authentication_invalid_format(client):
    response = client.post('/auth', data={
        'email': 'test@example.com',
        'password': 'short'
    })
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'formato inválido' in json_data['message']
