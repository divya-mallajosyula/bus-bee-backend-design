from datetime import datetime
from bson import ObjectId


def serialize_notification(doc):
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")),
        "user_id": str(doc.get("user_id")),
        "message": doc.get("message"),
        "eta_minutes": doc.get("eta_minutes"),
        "is_read": doc.get("is_read", False),
        "created_at": doc.get("created_at"),
    }


def create_notification(db, user_id, message, eta_minutes=None):
    notifications = db["notifications"]
    now = datetime.utcnow().isoformat()
    doc = {
        "user_id": ObjectId(user_id),
        "message": message,
        "eta_minutes": eta_minutes,
        "is_read": False,
        "created_at": now,
    }
    result = notifications.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_notification(doc)


def list_notifications(db, user_id):
    notifications = db["notifications"]
    cursor = notifications.find({"user_id": ObjectId(user_id)}).sort("created_at", -1)
    return [serialize_notification(doc) for doc in cursor]


def mark_notification_read(db, notification_id):
    notifications = db["notifications"]
    notifications.update_one({"_id": ObjectId(notification_id)}, {"$set": {"is_read": True}})
    return serialize_notification(notifications.find_one({"_id": ObjectId(notification_id)}))
