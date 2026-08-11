from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.chatbot_service import generate_answer

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api/chatbot")


@chatbot_bp.route("/ask", methods=["POST"])
@jwt_required()
def ask():
    data = request.get_json() or {}
    message = data.get("message", "")
    context = data.get("context", {})

    if not message.strip():
        return jsonify({"error": "message is required"}), 400

    result = generate_answer(message, context)
    return jsonify(result)
