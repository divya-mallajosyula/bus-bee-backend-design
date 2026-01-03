from datetime import datetime
from bson import ObjectId


def serialize_payment(doc):
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")),
        "user_id": str(doc.get("user_id")),
        "booking_id": str(doc.get("booking_id")),
        "amount": doc.get("amount"),
        "payment_method": doc.get("payment_method"),
        "status": doc.get("status"),
        "invoice_pdf_url": doc.get("invoice_pdf_url"),
        "timestamp": doc.get("timestamp"),
    }


def create_payment(db, user_id, booking_id, amount, payment_method, status, invoice_pdf_url=None):
    payments = db["payments"]
    now = datetime.utcnow().isoformat()
    doc = {
        "user_id": ObjectId(user_id),
        "booking_id": ObjectId(booking_id),
        "amount": amount,
        "payment_method": payment_method,
        "status": status,
        "invoice_pdf_url": invoice_pdf_url,
        "timestamp": now,
    }
    result = payments.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_payment(doc)


def find_payments_by_user(db, user_id):
    payments = db["payments"]
    cursor = payments.find({"user_id": ObjectId(user_id)}).sort("timestamp", -1)
    return [serialize_payment(doc) for doc in cursor]


def find_payment_by_invoice(db, invoice_id):
    payments = db["payments"]
    return serialize_payment(payments.find_one({"invoice_pdf_url": {"$regex": invoice_id}}))
