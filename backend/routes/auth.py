from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jti
from extensions import db, bcrypt
from models import User, UserSettings, LoginActivity, Session

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name, email, password = data.get("name"), data.get("email"), data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    user = User(
        name=name,
        email=email,
        password_hash=bcrypt.generate_password_hash(password).decode("utf-8"),
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    db.session.add(Session(
        user_id=user.id,
        jti=get_jti(token),
        device_info=request.headers.get("User-Agent", "")[:255],
        ip_address=request.remote_addr or "",
    ))
    db.session.commit()

    return jsonify({"token": token, "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email, password = data.get("email"), data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password or ""):
        return jsonify({"error": "Invalid email or password"}), 401

    settings = UserSettings.query.filter_by(user_id=user.id).first()

    # Log this login attempt (for the Login Activity setting)
    db.session.add(LoginActivity(
        user_id=user.id,
        ip_address=request.remote_addr or "",
        user_agent=request.headers.get("User-Agent", "")[:255],
    ))
    db.session.commit()

    if settings and settings.two_factor_enabled:
        return jsonify({"requires_2fa": True, "user_id": user.id}), 200

    token = create_access_token(identity=str(user.id))
    db.session.add(Session(
        user_id=user.id,
        jti=get_jti(token),
        device_info=request.headers.get("User-Agent", "")[:255],
        ip_address=request.remote_addr or "",
    ))
    db.session.commit()

    return jsonify({"token": token, "user": user.to_dict()}), 200


@auth_bp.route("/verify-2fa", methods=["POST"])
def verify_2fa():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    pin = data.get("pin", "")

    user = User.query.get(user_id)
    settings = UserSettings.query.filter_by(user_id=user_id).first() if user else None

    if not user or not settings or not settings.two_factor_enabled:
        return jsonify({"error": "Invalid request"}), 400

    if not bcrypt.check_password_hash(settings.two_factor_pin_hash, pin):
        return jsonify({"error": "Incorrect PIN"}), 401

    token = create_access_token(identity=str(user.id))
    db.session.add(Session(
        user_id=user.id,
        jti=get_jti(token),
        device_info=request.headers.get("User-Agent", "")[:255],
        ip_address=request.remote_addr or "",
    ))
    db.session.commit()

    return jsonify({"token": token, "user": user.to_dict()}), 200