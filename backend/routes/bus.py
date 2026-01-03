from flask import Blueprint, request, jsonify, current_app
from models.bus import find_buses_by_location, find_bus_by_id

bus_bp = Blueprint("bus", __name__)


@bus_bp.get("/search")
def search_buses():
    location = request.args.get("location", "")
    if not location:
        return jsonify({"error": "location is required"}), 400
    db = current_app.db
    buses = find_buses_by_location(db, location)
    return jsonify(buses)


@bus_bp.get("/<bus_id>")
def get_bus(bus_id):
    db = current_app.db
    bus = find_bus_by_id(db, bus_id)
    if not bus:
        return jsonify({"error": "Bus not found"}), 404
    return jsonify(bus)
