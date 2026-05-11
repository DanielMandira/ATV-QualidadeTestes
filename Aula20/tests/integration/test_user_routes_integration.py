def test_create_user_missing_name_returns_400(client):
    response = client.post("/users", json={})

    assert response.status_code == 400
    assert response.get_json()["error"] == "name is required"


def test_create_user_duplicate_returns_400(client):
    client.post("/users", json={"name": "Ana"})

    response = client.post("/users", json={"name": "Ana"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "User already exists"


def test_update_user_duplicate_name_returns_400(client):
    client.post("/users", json={"name": "Ana"})
    user2 = client.post("/users", json={"name": "Bia"}).get_json()

    response = client.put(f"/users/{user2['id']}", json={"name": "Ana"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "User already exists"


def test_delete_user_not_found_returns_404(client):
    response = client.delete("/users/123")

    assert response.status_code == 404


def test_list_users_filters_by_name_query(client):
    client.post("/users", json={"name": "Alice"})
    client.post("/users", json={"name": "Alicia"})
    client.post("/users", json={"name": "Bob"})

    response = client.get("/users?name=ali")

    assert response.status_code == 200
    names = [user["name"] for user in response.get_json()]
    assert names == ["Alice", "Alicia"]
