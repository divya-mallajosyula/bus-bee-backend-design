from datetime import datetime
from bson import ObjectId


def serialize_user(doc):
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "email": doc.get("email"),
        "phone": doc.get("phone"),
        "preferred_language": doc.get("preferred_language", "en"),
        "created_at": doc.get("created_at"),
    }


def create_user(db, name, email, phone, password_hash, preferred_language="en"):
    users = db["users"]
    now = datetime.utcnow().isoformat()
    doc = {
        "name": name,
        "email": email.lower(),
        "phone": phone,
        "password_hash": password_hash,
        "preferred_language": preferred_language,
        "created_at": now,
    }
    result = users.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_user(doc)


def find_by_email_or_phone(db, email_or_phone):
    users = db["users"]
    return users.find_one({"$or": [{"email": email_or_phone.lower()}, {"phone": email_or_phone}]})


def find_user_by_id(db, user_id):
    users = db["users"]
    return users.find_one({"_id": ObjectId(user_id)})


def update_user(db, user_id, updates):
    users = db["users"]
    users.update_one({"_id": ObjectId(user_id)}, {"$set": updates})
    return find_user_by_id(db, user_id)
