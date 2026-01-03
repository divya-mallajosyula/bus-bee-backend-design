from flask import Blueprint, request, jsonify, current_app
from utils.password_hash import hash_password, check_password
from utils.jwt_handler import generate_token, token_required
from models.user import create_user, find_by_email_or_phone, find_user_by_id, update_user, serialize_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(force=True)
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    preferred_language = data.get("preferred_language", "en")

    if not all([name, email, phone, password]):
        return jsonify({"error": "Missing required fields"}), 400

    db = current_app.db
    if find_by_email_or_phone(db, email) or find_by_email_or_phone(db, phone):
        return jsonify({"error": "User already exists"}), 409

    pwd_hash = hash_password(password)
    user = create_user(db, name, email, phone, pwd_hash, preferred_language)
    token = generate_token(user["id"])
    return jsonify({"user": user, "token": token})


@auth_bp.post("/login")
def login():
    data = request.get_json(force=True)
    credential = data.get("credential")  # email or phone
    password = data.get("password")
    if not credential or not password:
        return jsonify({"error": "Missing credentials"}), 400

    db = current_app.db
    user_doc = find_by_email_or_phone(db, credential)
    if not user_doc or not check_password(password, user_doc.get("password_hash", "")):
        return jsonify({"error": "Invalid credentials"}), 401

    user = serialize_user(user_doc)
    token = generate_token(user["id"])
    return jsonify({"user": user, "token": token})


@auth_bp.get("/profile")
@token_required
def get_profile():
    db = current_app.db
    user = serialize_user(find_user_by_id(db, request.user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@auth_bp.put("/profile")
@token_required
def update_profile():
    data = request.get_json(force=True)
    allowed_fields = {"name", "phone", "preferred_language"}
    updates = {k: v for k, v in data.items() if k in allowed_fields and v}
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400

    db = current_app.db
    user_doc = update_user(db, request.user_id, updates)
    user = serialize_user(user_doc)
    return jsonify(user)
