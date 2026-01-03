from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

from routes.auth import auth_bp
from routes.bus import bus_bp
from routes.booking import booking_bp
from routes.payment import payment_bp
from routes.chatbot import chatbot_bp
from routes.translate import translate_bp
from routes.notification import notification_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/busbee")
    client = MongoClient(mongo_uri)
    app.db = client.get_default_database()

    app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "change_me")
    app.config["JWT_ALGORITHM"] = os.getenv("JWT_ALGORITHM","HS256")
    app.config["JWT_EXPIRE_MINUTES"] = int(os.getenv("JWT_EXPIRE_MINUTES", 60))
    app.config["PDF_STORAGE_PATH"] = os.getenv("PDF_STORAGE_PATH", os.path.join(os.getcwd(), "uploads"))



    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(bus_bp, url_prefix="/api/buses")
    app.register_blueprint(booking_bp, url_prefix="/api/bookings")
    app.register_blueprint(payment_bp, url_prefix="/api/payments")
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
    app.register_blueprint(translate_bp, url_prefix="/api/translate")
    app.register_blueprint(notification_bp, url_prefix="/api/notifications")

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
