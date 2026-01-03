from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

import config
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

    client = MongoClient(config.MONGO_URI)
    app.db = client.get_default_database()

    app.config["JWT_SECRET"] = config.JWT_SECRET
    app.config["JWT_ALGORITHM"] = config.JWT_ALGORITHM
    app.config["PDF_STORAGE_PATH"] = config.PDF_STORAGE_PATH
    app.config["JWT_EXPIRE_MINUTES"] = config.TOKEN_EXPIRE_MINUTES

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
