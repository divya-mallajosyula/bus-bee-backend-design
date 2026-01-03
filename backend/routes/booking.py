from flask import Blueprint, request, jsonify, current_app
from utils.jwt_handler import token_required
from models.booking import create_booking, find_bookings_by_user
from models.bus import find_bus_by_id

booking_bp = Blueprint("booking", __name__)


def _calculate_total(bus, seat_count):
    return (bus.get("price") or 0) * seat_count


@booking_bp.post("/create")
@token_required
def create_booking_route():
    data = request.get_json(force=True)
    bus_id = data.get("bus_id")
    seat_count = int(data.get("seat_count", 1))

    if not bus_id or seat_count <= 0:
        return jsonify({"error": "bus_id and seat_count are required"}), 400

    db = current_app.db
    bus = find_bus_by_id(db, bus_id)
    if not bus:
        return jsonify({"error": "Bus not found"}), 404

    total_amount = _calculate_total(bus, seat_count)
    booking = create_booking(db, request.user_id, bus_id, seat_count, total_amount)
    return jsonify(booking), 201


@booking_bp.get("/user/<user_id>")
@token_required
def list_user_bookings(user_id):
    db = current_app.db
    bookings = find_bookings_by_user(db, user_id)
    return jsonify(bookings)
