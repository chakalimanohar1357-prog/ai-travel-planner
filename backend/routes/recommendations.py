from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Destination, Trip, Hotel, Restaurant, Attraction
from services.recommendation_engine import rank_destinations, rank_items

recommendations_bp = Blueprint("recommendations", __name__, url_prefix="/api/recommendations")


@recommendations_bp.route("/destinations", methods=["POST"])
@jwt_required()
def recommend_destinations():
    data = request.get_json() or {}
    interests = data.get("interests", [])
    budget = float(data.get("budget", 500))
    duration_days = int(data.get("duration_days", 5)) or 5
    budget_per_day = budget / duration_days

    destinations = Destination.query.all()
    all_trips = Trip.query.all()

    ranked = rank_destinations(destinations, all_trips, interests, budget_per_day)
    return jsonify({"recommendations": ranked[:10]})


@recommendations_bp.route("/destinations/<int:destination_id>/attractions", methods=["GET"])
@jwt_required()
def recommend_attractions(destination_id):
    interests = request.args.getlist("interest")
    attractions = Attraction.query.filter_by(destination_id=destination_id).all()
    ranked = rank_items(attractions, interests, item_type="attraction")
    return jsonify({"attractions": [a.to_dict() for a in ranked]})


@recommendations_bp.route("/destinations/<int:destination_id>/hotels", methods=["GET"])
@jwt_required()
def recommend_hotels(destination_id):
    category = request.args.get("category")
    query = Hotel.query.filter_by(destination_id=destination_id)
    if category:
        query = query.filter_by(category=category)
    hotels = rank_items(query.all(), [], item_type="hotel")
    return jsonify({"hotels": [h.to_dict() for h in hotels]})


@recommendations_bp.route("/destinations/<int:destination_id>/restaurants", methods=["GET"])
@jwt_required()
def recommend_restaurants(destination_id):
    restaurants = Restaurant.query.filter_by(destination_id=destination_id).all()
    ranked = rank_items(restaurants, [], item_type="restaurant")
    return jsonify({"restaurants": [r.to_dict() for r in ranked]})
