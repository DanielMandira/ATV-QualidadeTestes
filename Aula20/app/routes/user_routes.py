from flask import Blueprint, jsonify, request

from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    filter_users_by_name,
    normalize_name,
    is_duplicate_name,
)

user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("", methods=["GET"])
def list_users():
    query = request.args.get("name")
    if query is None:
        return jsonify(get_all_users()), 200

    return jsonify(filter_users_by_name(query)), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@user_bp.route("", methods=["POST"])
def create():
    data = request.get_json(silent=True) or {}
    name = normalize_name(data.get("name", ""))
    if not name:
        return jsonify({"error": "name is required"}), 400

    user = create_user({"name": name})
    if user is None:
        return jsonify({"error": "User already exists"}), 400
    return jsonify(user), 201


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update(user_id):
    data = request.get_json(silent=True) or {}
    name = normalize_name(data.get("name", ""))
    if not name:
        return jsonify({"error": "name is required"}), 400

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if is_duplicate_name(name, ignore_id=user_id):
        return jsonify({"error": "User already exists"}), 400

    updated_user = update_user(user_id, {"name": name})
    return jsonify(updated_user), 200


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    delete_user(user_id)
    return "", 204
