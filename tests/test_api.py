
import pytest
from app import create_app
from models import db


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def create_user(client):
    return client.post("/api/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "role": "operator"
    })


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200


def test_create_user(client):
    response = create_user(client)
    assert response.status_code == 201


def test_invalid_user(client):
    response = client.post("/api/users", json={
        "name": "Test"
    })
    assert response.status_code == 400


def test_duplicate_user(client):
    create_user(client)
    response = create_user(client)
    assert response.status_code == 409


def test_update_user(client):
    user = create_user(client).json["data"]

    response = client.put(
        f"/api/users/{user['id']}",
        json={
            "name": "Updated User",
            "email": "test@example.com",
            "role": "admin"
        }
    )

    assert response.status_code == 200


def test_delete_user(client):
    user = create_user(client).json["data"]

    response = client.delete(
        f"/api/users/{user['id']}"
    )

    assert response.status_code == 200


def test_user_not_found(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404


def test_create_device(client):
    user = create_user(client).json["data"]

    response = client.post("/api/devices", json={
        "user_id": user["id"],
        "name": "Smart Bin Test",
        "location": "Laboratorium",
        "status": "online"
    })

    assert response.status_code == 201


def test_invalid_device(client):
    response = client.post("/api/devices", json={
        "user_id": 999,
        "name": "Smart Bin",
        "location": "Kampus",
        "status": "online"
    })

    assert response.status_code == 400