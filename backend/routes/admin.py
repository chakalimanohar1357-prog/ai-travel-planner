from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Destination, Hotel, Restaurant, Attraction, Trip

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = User.query.get(int(get_jwt_identity()))
        if not user or user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


# ---------------- TEMPORARY: one-time database seed ----------------
# Remove this route once the database has been confirmed seeded.

@admin_bp.route("/seed-database", methods=["GET"])
def seed_database_once():
    secret = request.args.get("key", "")
    if secret != current_app.config.get("SECRET_KEY"):
        return jsonify({"error": "Unauthorized"}), 403

    from data.seed_data import seed
    seed()
    return jsonify({"message": "Database seeded successfully"})


@admin_bp.route("/stats", methods=["GET"])
@admin_required
def stats():
    return jsonify({
        "total_users": User.query.count(),
        "total_destinations": Destination.query.count(),
        "total_trips": Trip.query.count(),
        "total_hotels": Hotel.query.count(),
        "total_restaurants": Restaurant.query.count(),
    })


@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    users = User.query.all()
    return jsonify({"users": [u.to_dict() for u in users]})


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})


# ---------------- Destinations CRUD ----------------

@admin_bp.route("/destinations", methods=["POST"])
@admin_required
def create_destination():
    data = request.get_json() or {}
    dest = Destination(
        name=data.get("name"), country=data.get("country"),
        description=data.get("description", ""),
        tags=",".join(data.get("tags", [])),
        avg_daily_cost=data.get("avg_daily_cost", 50),
        latitude=data.get("latitude"), longitude=data.get("longitude"),
        popularity_score=data.get("popularity_score", 0.5),
        image_url=data.get("image_url", ""),
    )
    db.session.add(dest)
    db.session.commit()
    return jsonify({"destination": dest.to_dict()}), 201


@admin_bp.route("/destinations/<int:destination_id>", methods=["PUT"])
@admin_required
def update_destination(destination_id):
    dest = Destination.query.get(destination_id)
    if not dest:
        return jsonify({"error": "Destination not found"}), 404
    data = request.get_json() or {}
    for field in ("name", "country", "description", "avg_daily_cost",
                  "latitude", "longitude", "popularity_score", "image_url"):
        if field in data:
            setattr(dest, field, data[field])
    if "tags" in data:
        dest.tags = ",".join(data["tags"])
    db.session.commit()
    return jsonify({"destination": dest.to_dict()})


@admin_bp.route("/destinations/<int:destination_id>", methods=["DELETE"])
@admin_required
def delete_destination(destination_id):
    dest = Destination.query.get(destination_id)
    if not dest:
        return jsonify({"error": "Destination not found"}), 404
    db.session.delete(dest)
    db.session.commit()
    return jsonify({"message": "Destination deleted"})


# ---------------- Hotels / Restaurants CRUD (lightweight) ----------------

@admin_bp.route("/hotels", methods=["POST"])
@admin_required
def create_hotel():
    data = request.get_json() or {}
    hotel = Hotel(**data)
    db.session.add(hotel)
    db.session.commit()
    return jsonify({"hotel": hotel.to_dict()}), 201


@admin_bp.route("/hotels/<int:hotel_id>", methods=["DELETE"])
@admin_required
def delete_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404
    db.session.delete(hotel)
    db.session.commit()
    return jsonify({"message": "Hotel deleted"})


@admin_bp.route("/restaurants", methods=["POST"])
@admin_required
def create_restaurant():
    data = request.get_json() or {}
    restaurant = Restaurant(**data)
    db.session.add(restaurant)
    db.session.commit()
    return jsonify({"restaurant": restaurant.to_dict()}), 201


@admin_bp.route("/restaurants/<int:restaurant_id>", methods=["DELETE"])
@admin_required
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({"message": "Restaurant deleted"})


@admin_bp.route("/attractions", methods=["POST"])
@admin_required
def create_attraction():
    data = request.get_json() or {}
    attraction = Attraction(**data)
    db.session.add(attraction)
    db.session.commit()
    return jsonify({"attraction": attraction.to_dict()}), 201


@admin_bp.route("/attractions/<int:attraction_id>", methods=["DELETE"])
@admin_required
def delete_attraction(attraction_id):
    attraction = Attraction.query.get(attraction_id)
    if not attraction:
        return jsonify({"error": "Attraction not found"}), 404
    db.session.delete(attraction)
    db.session.commit()
    return jsonify({"message": "Attraction deleted"})