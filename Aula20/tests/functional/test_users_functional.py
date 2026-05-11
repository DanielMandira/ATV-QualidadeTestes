import sys
from pathlib import Path

# Add Aula18 to sys.path to allow imports from app
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from app import create_app
from app.services import user_service


@pytest.fixture
def client():
    app = create_app()
    user_service.users.clear()
    user_service.current_id = 1

    return app.test_client()


def test_user_flow(client):
    # Create user
    response = client.post("/users", json={"name": "Maylon"})
    assert response.status_code == 201
    user = response.get_json()
    user_id = user["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200

    response = client.put(f"/users/{user_id}", json={"name": "Novo Nome"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Novo Nome"

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_list_users(client):
    client.post("/users", json={"name": "User 1"})
    client.post("/users", json={"name": "User 2"})

    response = client.get("/users")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2


def test_list_users_with_three_users(client):
    client.post("/users", json={"name": "User 1"})
    client.post("/users", json={"name": "User 2"})
    client.post("/users", json={"name": "User 3"})

    response = client.get("/users")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 3
