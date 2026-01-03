from datetime import datetime
from bson import ObjectId


def serialize_booking(doc):
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")),
        "user_id": str(doc.get("user_id")),
        "bus_id": str(doc.get("bus_id")),
        "seat_count": doc.get("seat_count"),
        "total_amount": doc.get("total_amount"),
        "payment_status": doc.get("payment_status"),
        "invoice_id": doc.get("invoice_id"),
        "booking_time": doc.get("booking_time"),
    }


def create_booking(db, user_id, bus_id, seat_count, total_amount, payment_status="PENDING", invoice_id=None):
    bookings = db["bookings"]
    now = datetime.utcnow().isoformat()
    doc = {
        "user_id": ObjectId(user_id),
        "bus_id": ObjectId(bus_id),
        "seat_count": seat_count,
        "total_amount": total_amount,
        "payment_status": payment_status,
        "invoice_id": invoice_id,
        "booking_time": now,
    }
    result = bookings.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_booking(doc)


def update_booking_status(db, booking_id, status, invoice_id=None):
    bookings = db["bookings"]
    update_doc = {"payment_status": status}
    if invoice_id:
        update_doc["invoice_id"] = invoice_id
    bookings.update_one({"_id": ObjectId(booking_id)}, {"$set": update_doc})
    return serialize_booking(bookings.find_one({"_id": ObjectId(booking_id)}))


def find_bookings_by_user(db, user_id):
    bookings = db["bookings"]
    cursor = bookings.find({"user_id": ObjectId(user_id)}).sort("booking_time", -1)
    return [serialize_booking(doc) for doc in cursor]
