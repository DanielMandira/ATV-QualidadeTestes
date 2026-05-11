from app.services import user_service


def test_create_user_assigns_incrementing_id():
    user1 = user_service.create_user({"name": "Ana"})
    user2 = user_service.create_user({"name": "Bruno"})

    assert user1["id"] == 1
    assert user2["id"] == 2


def test_create_user_stores_user():
    user_service.create_user({"name": "Ana"})

    assert len(user_service.get_all_users()) == 1


def test_create_user_rejects_duplicate_name_case_insensitive():
    user_service.create_user({"name": "Ana"})

    duplicate = user_service.create_user({"name": "ana"})

    assert duplicate is None


def test_create_user_rejects_blank_name():
    created = user_service.create_user({"name": "   "})

    assert created is None
    assert len(user_service.get_all_users()) == 0


def test_get_user_by_id_returns_user():
    created = user_service.create_user({"name": "Carlos"})

    found = user_service.get_user_by_id(created["id"])

    assert found == created


def test_get_user_by_id_returns_none_when_missing():
    assert user_service.get_user_by_id(999) is None


def test_update_user_updates_name():
    created = user_service.create_user({"name": "Daniel"})

    updated = user_service.update_user(created["id"], {"name": "Dani"})

    assert updated["name"] == "Dani"


def test_update_user_returns_none_when_missing():
    assert user_service.update_user(999, {"name": "Nope"}) is None


def test_delete_user_removes_user():
    created = user_service.create_user({"name": "Eva"})

    user_service.delete_user(created["id"])

    assert user_service.get_user_by_id(created["id"]) is None


def test_delete_user_keeps_other_users():
    user1 = user_service.create_user({"name": "Fabio"})
    user2 = user_service.create_user({"name": "Gabi"})

    user_service.delete_user(user1["id"])

    assert user_service.get_user_by_id(user2["id"]) == user2
    assert len(user_service.get_all_users()) == 1


def test_filter_users_by_name_returns_matching_subset():
    user_service.create_user({"name": "Alice"})
    user_service.create_user({"name": "Bob"})
    user_service.create_user({"name": "Alicia"})

    filtered = user_service.filter_users_by_name("ali")
    filtered_names = [user["name"] for user in filtered]

    assert filtered_names == ["Alice", "Alicia"]


def test_filter_users_by_name_returns_all_when_query_blank():
    user_service.create_user({"name": "Alice"})
    user_service.create_user({"name": "Bob"})

    filtered = user_service.filter_users_by_name("  ")

    assert len(filtered) == 2


def test_normalize_name_strips_whitespace():
    assert user_service.normalize_name("  Ana  ") == "Ana"


def test_is_duplicate_name_ignores_same_user_id():
    created = user_service.create_user({"name": "Ana"})

    assert user_service.is_duplicate_name("Ana", ignore_id=created["id"]) is False
