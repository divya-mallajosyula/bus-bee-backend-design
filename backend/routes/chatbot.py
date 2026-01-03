from flask import Blueprint, request, jsonify
from utils.jwt_handler import token_required
from models.bus import find_buses_by_location

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.post("/query")
@token_required
def chatbot_query():
    data = request.get_json(force=True)
    text = data.get("text", "") or data.get("voice_text", "")
    text = text.lower()
    location = data.get("location")
    intent = "general"

    if "bus" in text or location:
        intent = "bus_search"

    response = {"intent": intent, "reply": "How can I assist you?"}

    if intent == "bus_search" and location:
        from flask import current_app

        db = current_app.db
        buses = find_buses_by_location(db, location)
        response["reply"] = "Here are buses near you"
        response["buses"] = buses
    else:
        response["reply"] = "I can help you find buses, timings, ETA, and bookings."

    return jsonify(response)
