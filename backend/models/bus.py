from bson import ObjectId


def serialize_bus(doc):
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")),
        "bus_name": doc.get("bus_name"),
        "bus_type": doc.get("bus_type"),
        "route": doc.get("route", []),
        "departure_time": doc.get("departure_time"),
        "arrival_time": doc.get("arrival_time"),
        "price": doc.get("price"),
        "eta_minutes": doc.get("eta_minutes", None),
        "prebooking_available": doc.get("prebooking_available", False),
    }


def find_buses_by_location(db, location):
    buses = db["buses"]
    cursor = buses.find({"route": {"$regex": location, "$options": "i"}})
    return [serialize_bus(doc) for doc in cursor]


def find_bus_by_id(db, bus_id):
    buses = db["buses"]
    return serialize_bus(buses.find_one({"_id": ObjectId(bus_id)}))
