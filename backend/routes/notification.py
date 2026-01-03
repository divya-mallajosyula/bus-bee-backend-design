from flask import Blueprint, request, jsonify, current_app
from utils.jwt_handler import token_required
from models.notification import list_notifications, create_notification, mark_notification_read

notification_bp = Blueprint("notification", __name__)


@notification_bp.get("/user/<user_id>")
@token_required
def get_notifications(user_id):
    db = current_app.db
    items = list_notifications(db, user_id)
    return jsonify(items)


@notification_bp.post("/create")
@token_required
def create_notification_route():
    data = request.get_json(force=True)
    user_id = data.get("user_id")
    message = data.get("message")
    eta_minutes = data.get("eta_minutes")
    if not user_id or not message:
        return jsonify({"error": "user_id and message are required"}), 400

    db = current_app.db
    notif = create_notification(db, user_id, message, eta_minutes)
    return jsonify(notif), 201


@notification_bp.post("/<notification_id>/read")
@token_required
def mark_read(notification_id):
    db = current_app.db
    notif = mark_notification_read(db, notification_id)
    return jsonify(notif)
