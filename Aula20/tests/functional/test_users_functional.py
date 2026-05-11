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


def test_create_user_rejects_blank_name(client):
    response = client.post("/users", json={"name": "   "})

    assert response.status_code == 400
    assert response.get_json()["error"] == "name is required"


def test_update_user_not_found(client):
    response = client.put("/users/999", json={"name": "Novo Nome"})

    assert response.status_code == 404


def test_filter_users_by_name_partial_match(client):
    client.post("/users", json={"name": "Maria"})
    client.post("/users", json={"name": "Joana"})
    client.post("/users", json={"name": "Carlos"})

    response = client.get("/users?name=ana")
    data = response.get_json()

    assert response.status_code == 200
    assert [user["name"] for user in data] == ["Joana"]
