def test_should_not_allow_duplicate_users():
    from app.services import user_service

    user_service.users.clear()
    user_service.current_id = 1

    user_service.create_user({"name": "Maylon"})


    users =user_service.create_user({"name": "Maylon"})
    assert user is None
    
def create_user(data):
    global current_id
    
    existing_user = next((u for u in users if u["name"] == data["name"]), None)
    
    if existing_user:
        return None
    
    user = {"id": current_id, "name": data["name"]}
    
    users.append(user)
    current_id += 1
    
    return user

def test_should_return_400_when_user_already_exists(client):
    client.post("/users", json={"name": "Maylon"})
    
    response = client.post("/users", json={"name": "Maylon"})
    
    assert response.status_code == 400
    
    
