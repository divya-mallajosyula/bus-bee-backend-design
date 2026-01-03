import requests
from flask import Blueprint, request, jsonify, current_app
from utils.jwt_handler import token_required
import config

translate_bp = Blueprint("translate", __name__)


@translate_bp.post("")
@token_required
def translate_text():
    data = request.get_json(force=True)
    text = data.get("text")
    target_language = data.get("target_language")
    if not text or not target_language:
        return jsonify({"error": "text and target_language are required"}), 400

    api_key = config.TRANSLATION_API_KEY
    if not api_key:
        return jsonify({"error": "Translation API key not configured"}), 500

    # Replace with real translation provider
    response = requests.post(
        "https://api.example-translate.com/v1/translate",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"text": text, "target_language": target_language},
        timeout=5,
    )
    if response.status_code != 200:
        return jsonify({"error": "Translation service failed"}), 502

    translated = response.json().get("translated_text")
    return jsonify({"translated_text": translated})
