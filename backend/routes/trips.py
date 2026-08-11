import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Trip, Destination, Hotel, Restaurant, Attraction, Favorite
from services.recommendation_engine import rank_items
from services.itinerary_generator import generate_itinerary, estimate_total_cost
from services.packing_list import generate_packing_list
from services.cost_estimator import check_budget_feasibility

trips_bp = Blueprint("trips", __name__, url_prefix="/api/trips")


@trips_bp.route("/plan", methods=["POST"])
@jwt_required()
def plan_trip():
    """
    Core AI itinerary generation endpoint.
    Body: { destination_id, budget, duration_days, travelers, interests[],
            transport_mode, accommodation_pref, weather_condition }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    destination = Destination.query.get(data.get("destination_id"))
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    interests = data.get("interests", [])
    duration_days = int(data.get("duration_days", 3)) or 3
    travelers = int(data.get("travelers", 1)) or 1
    budget = float(data.get("budget", 500))
    transport_mode = data.get("transport_mode", "flight")
    accommodation_pref = data.get("accommodation_pref", "mid-range")
    weather_condition = data.get("weather_condition", "mild")

    daily_budget = budget / duration_days if duration_days else budget

    attractions = Attraction.query.filter_by(destination_id=destination.id).all()
    ranked_attractions = rank_items(attractions, interests, item_type="attraction")
    hotels = Hotel.query.filter_by(destination_id=destination.id).all()
    restaurants = Restaurant.query.filter_by(destination_id=destination.id).all()

    itinerary = generate_itinerary(
        destination, ranked_attractions, restaurants, hotels,
        duration_days, accommodation_pref, daily_budget,
    )
    cost_breakdown = estimate_total_cost(itinerary, travelers, transport_mode, duration_days)
    feasibility = check_budget_feasibility(cost_breakdown["total"], budget)
    packing_list = generate_packing_list(interests, duration_days, weather_condition, travelers)

    trip = Trip(
        user_id=user_id,
        destination_id=destination.id,
        destination_name=destination.name,
        budget=budget,
        duration_days=duration_days,
        travelers=travelers,
        interests=",".join(interests),
        transport_mode=transport_mode,
        accommodation_pref=accommodation_pref,
        itinerary_json=json.dumps(itinerary),
        estimated_cost=cost_breakdown["total"],
        status="planned",
    )
    db.session.add(trip)
    db.session.commit()

    return jsonify({
        "trip": trip.to_dict(),
        "cost_breakdown": cost_breakdown,
        "budget_feasibility": feasibility,
        "packing_list": packing_list,
    }), 201


@trips_bp.route("", methods=["GET"])
@jwt_required()
def get_my_trips():
    user_id = int(get_jwt_identity())
    trips = Trip.query.filter_by(user_id=user_id).order_by(Trip.created_at.desc()).all()
    return jsonify({"trips": [t.to_dict() for t in trips]})


@trips_bp.route("/<int:trip_id>", methods=["GET"])
@jwt_required()
def get_trip(trip_id):
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    return jsonify({"trip": trip.to_dict()})


@trips_bp.route("/<int:trip_id>/packing-list", methods=["GET"])
@jwt_required()
def get_packing_list(trip_id):
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    interests = trip.interests.split(",") if trip.interests else []
    packing_list = generate_packing_list(interests, trip.duration_days, "mild", trip.travelers)
    return jsonify({"packing_list": packing_list})


@trips_bp.route("/<int:trip_id>", methods=["DELETE"])

@jwt_required()
def delete_trip(trip_id):
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    db.session.delete(trip)
    db.session.commit()
    return jsonify({"message": "Trip deleted"})


@trips_bp.route("/<int:trip_id>/status", methods=["PATCH"])
@jwt_required()
def update_trip_status(trip_id):
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    status = (request.get_json() or {}).get("status")
    if status not in ("planned", "ongoing", "completed"):
        return jsonify({"error": "Invalid status"}), 400
    trip.status = status
    db.session.commit()
    return jsonify({"trip": trip.to_dict()})


# ---------------- Favorites ----------------

@trips_bp.route("/favorites", methods=["GET"])
@jwt_required()
def get_favorites():
    user_id = int(get_jwt_identity())
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    destinations = [Destination.query.get(f.destination_id).to_dict() for f in favorites if Destination.query.get(f.destination_id)]
    return jsonify({"favorites": destinations})


@trips_bp.route("/favorites/<int:destination_id>", methods=["POST"])
@jwt_required()
def add_favorite(destination_id):
    user_id = int(get_jwt_identity())
    if Favorite.query.filter_by(user_id=user_id, destination_id=destination_id).first():
        return jsonify({"message": "Already in favorites"}), 200
    fav = Favorite(user_id=user_id, destination_id=destination_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Added to favorites"}), 201


@trips_bp.route("/favorites/<int:destination_id>", methods=["DELETE"])
@jwt_required()
def remove_favorite(destination_id):
    user_id = int(get_jwt_identity())
    fav = Favorite.query.filter_by(user_id=user_id, destination_id=destination_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
    return jsonify({"message": "Removed from favorites"})
