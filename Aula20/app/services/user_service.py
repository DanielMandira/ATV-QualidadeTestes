users = []
current_id = 1


def reset_state():
    global current_id
    users.clear()
    current_id = 1


def normalize_name(name):
    return name.strip()


def is_duplicate_name(name, ignore_id=None):
    normalized = normalize_name(name).lower()
    for user in users:
        if ignore_id is not None and user["id"] == ignore_id:
            continue
        if user["name"].lower() == normalized:
            return True
    return False


def get_all_users():
    return users


def get_user_by_id(user_id):
    return next((u for u in users if u["id"] == user_id), None)


def create_user(data):
    global current_id
    name = normalize_name(data["name"])
    if not name:
        return None
    if is_duplicate_name(name):
        return None

    user = {"id": current_id, "name": name}
    users.append(user)
    current_id += 1
    return user


def update_user(user_id, data):
    user = get_user_by_id(user_id)
    if not user:
        return None

    user["name"] = normalize_name(data["name"])
    return user


def delete_user(user_id):
    users[:] = [u for u in users if u["id"] != user_id]


def filter_users_by_name(query):
    if query is None:
        return users

    normalized = normalize_name(query)
    if not normalized:
        return users

    normalized = normalized.lower()
    return [user for user in users if normalized in user["name"].lower()]
