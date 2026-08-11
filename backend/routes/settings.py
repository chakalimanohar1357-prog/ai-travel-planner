import json
import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from extensions import db, bcrypt
from models import (
    User, UserSettings, LoginActivity, Trip, Favorite, Review, Booking,
    Session, BlockedDestination, Feedback, Destination
)

settings_bp = Blueprint("settings", __name__, url_prefix="/api/settings")


def _get_or_create_settings(user_id):
    settings = UserSettings.query.filter_by(user_id=user_id).first()
    if not settings:
        settings = UserSettings(user_id=user_id)
        db.session.add(settings)
        db.session.commit()
    return settings


@settings_bp.route("", methods=["GET"])
@jwt_required()
def get_settings():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    settings = _get_or_create_settings(user_id)
    return jsonify({"profile": user.to_dict(), "settings": settings.to_dict()})


@settings_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}
    new_email = data.get("email", "").strip()

    if new_email and new_email != user.email:
        if User.query.filter_by(email=new_email).first():
            return jsonify({"error": "That email is already in use"}), 409
        user.email = new_email

    if data.get("name"):
        user.name = data["name"].strip()

    db.session.commit()
    return jsonify({"profile": user.to_dict()})


@settings_bp.route("/password", methods=["PUT"])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}
    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")

    if not bcrypt.check_password_hash(user.password_hash, current_password):
        return jsonify({"error": "Current password is incorrect"}), 401
    if len(new_password) < 6:
        return jsonify({"error": "New password must be at least 6 characters"}), 400

    user.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
    db.session.commit()
    return jsonify({"message": "Password updated successfully"})


@settings_bp.route("/preferences", methods=["PUT"])
@jwt_required()
def update_preferences():
    user_id = int(get_jwt_identity())
    settings = _get_or_create_settings(user_id)
    data = request.get_json() or {}

    if "currency" in data:
        settings.currency = data["currency"]
    if "language" in data:
        settings.language = data["language"]
    if "default_budget" in data:
        settings.default_budget = float(data["default_budget"])
    if "default_duration_days" in data:
        settings.default_duration_days = int(data["default_duration_days"])
    if "default_interests" in data:
        settings.default_interests = ",".join(data["default_interests"])

    db.session.commit()
    return jsonify({"settings": settings.to_dict()})


@settings_bp.route("/notifications", methods=["PUT"])
@jwt_required()
def update_notifications():
    user_id = int(get_jwt_identity())
    settings = _get_or_create_settings(user_id)
    data = request.get_json() or {}

    if "email_notifications" in data:
        settings.email_notifications = bool(data["email_notifications"])

    db.session.commit()
    return jsonify({"settings": settings.to_dict()})


@settings_bp.route("/photo", methods=["PUT"])
@jwt_required()
def update_photo():
    user_id = int(get_jwt_identity())
    settings = _get_or_create_settings(user_id)
    data = request.get_json() or {}

    settings.profile_photo_url = data.get("photo_url", "").strip()
    db.session.commit()
    return jsonify({"settings": settings.to_dict()})


# ---------------- Two-Factor PIN ----------------

@settings_bp.route("/2fa/enable", methods=["POST"])
@jwt_required()
def enable_2fa():
    user_id = int(get_jwt_identity())
    settings = _get_or_create_settings(user_id)

    pin = "".join(random.choices("0123456789", k=6))
    settings.two_factor_pin_hash = bcrypt.generate_password_hash(pin).decode("utf-8")
    settings.two_factor_enabled = True
    db.session.commit()

    # In a real product this PIN would be emailed/texted, never returned in
    # the API response. Returning it here once, for demo purposes only, so
    # you can see and test it without an SMS/email provider configured.
    return jsonify({
        "message": "Two-factor login enabled. Save this PIN -- it won't be shown again.",
        "pin": pin,
    })


@settings_bp.route("/2fa/disable", methods=["POST"])
@jwt_required()
def disable_2fa():
    user_id = int(get_jwt_identity())
    settings = _get_or_create_settings(user_id)
    settings.two_factor_enabled = False
    settings.two_factor_pin_hash = ""
    db.session.commit()
    return jsonify({"message": "Two-factor login disabled"})


# ---------------- Login activity ----------------

@settings_bp.route("/login-activity", methods=["GET"])
@jwt_required()
def get_login_activity():
    user_id = int(get_jwt_identity())
    activity = (
        LoginActivity.query.filter_by(user_id=user_id)
        .order_by(LoginActivity.created_at.desc())
        .limit(20)
        .all()
    )
    return jsonify({"activity": [a.to_dict() for a in activity]})


# ---------------- Active sessions ----------------

@settings_bp.route("/sessions", methods=["GET"])
@jwt_required()
def get_sessions():
    user_id = int(get_jwt_identity())
    sessions = (
        Session.query.filter_by(user_id=user_id, revoked=False)
        .order_by(Session.created_at.desc())
        .all()
    )
    return jsonify({"sessions": [s.to_dict() for s in sessions]})


@settings_bp.route("/sessions/<int:session_id>/revoke", methods=["POST"])
@jwt_required()
def revoke_session(session_id):
    user_id = int(get_jwt_identity())
    session = Session.query.filter_by(id=session_id, user_id=user_id).first()
    if not session:
        return jsonify({"error": "Session not found"}), 404
    session.revoked = True
    db.session.commit()
    return jsonify({"message": "Session revoked"})


# ---------------- Blocked destinations ----------------

@settings_bp.route("/blocked-destinations", methods=["GET"])
@jwt_required()
def get_blocked_destinations():
    user_id = int(get_jwt_identity())
    blocked = BlockedDestination.query.filter_by(user_id=user_id).all()
    destinations = [
        Destination.query.get(b.destination_id).to_dict()
        for b in blocked if Destination.query.get(b.destination_id)
    ]
    return jsonify({"blocked": destinations})


@settings_bp.route("/blocked-destinations/<int:destination_id>", methods=["POST"])
@jwt_required()
def block_destination(destination_id):
    user_id = int(get_jwt_identity())
    if not BlockedDestination.query.filter_by(user_id=user_id, destination_id=destination_id).first():
        db.session.add(BlockedDestination(user_id=user_id, destination_id=destination_id))
        db.session.commit()
    return jsonify({"message": "Destination blocked"})


@settings_bp.route("/blocked-destinations/<int:destination_id>", methods=["DELETE"])
@jwt_required()
def unblock_destination(destination_id):
    user_id = int(get_jwt_identity())
    b = BlockedDestination.query.filter_by(user_id=user_id, destination_id=destination_id).first()
    if b:
        db.session.delete(b)
        db.session.commit()
    return jsonify({"message": "Destination unblocked"})


# ---------------- Advanced preferences: units, home city, emergency contact, map style, accessibility ----------------

@settings_bp.route("/advanced-preferences", methods=["PUT"])
@jwt_required()
def update_advanced_preferences():
    user_id = int(get_jwt_identity())
    settings = _get_or_create_settings(user_id)
    data = request.get_json() or {}

    for field in ["unit_system", "home_city", "emergency_contact_name",
                  "emergency_contact_phone", "map_style", "font_size"]:
        if field in data:
            setattr(settings, field, data[field])
    if "high_contrast" in data:
        settings.high_contrast = bool(data["high_contrast"])

    db.session.commit()
    return jsonify({"settings": settings.to_dict()})


# ---------------- Data export ----------------

@settings_bp.route("/export", methods=["GET"])
@jwt_required()
def export_data():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    trips = Trip.query.filter_by(user_id=user_id).all()
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    reviews = Review.query.filter_by(user_id=user_id).all()
    bookings = Booking.query.filter_by(user_id=user_id).all()

    export = {
        "profile": user.to_dict(),
        "trips": [t.to_dict() for t in trips],
        "favorites": [f.to_dict() for f in favorites],
        "reviews": [r.to_dict() for r in reviews],
        "bookings": [b.to_dict() for b in bookings],
    }

    return jsonify(export)


# ---------------- Feedback / Contact us ----------------

@settings_bp.route("/feedback", methods=["POST"])
def submit_feedback():
    """Public -- works whether logged in or not, so the Contact page works for everyone."""
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Message is required"}), 400

    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        user_id = int(identity) if identity else None
    except Exception:
        pass

    feedback = Feedback(
        user_id=user_id,
        name=data.get("name", ""),
        email=data.get("email", ""),
        message=message,
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"message": "Thanks for your feedback!"}), 201


# ---------------- Delete account ----------------

@settings_bp.route("/account", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}
    password = data.get("password", "")
    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Incorrect password"}), 401

    UserSettings.query.filter_by(user_id=user_id).delete()
    LoginActivity.query.filter_by(user_id=user_id).delete()
    Session.query.filter_by(user_id=user_id).delete()
    BlockedDestination.query.filter_by(user_id=user_id).delete()
    Review.query.filter_by(user_id=user_id).delete()
    Booking.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)  # cascades to trips/favorites via relationship
    db.session.commit()

    return jsonify({"message": "Account deleted"})