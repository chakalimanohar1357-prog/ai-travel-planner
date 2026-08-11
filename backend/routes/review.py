from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Review, User, Destination, Trip

reviews_bp = Blueprint("reviews", __name__, url_prefix="/api/reviews")


@reviews_bp.route("/destinations/<int:destination_id>", methods=["GET"])
def get_reviews(destination_id):
    """Public endpoint - anyone can view reviews for a destination."""
    reviews = (
        Review.query.filter_by(destination_id=destination_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    result = []
    for r in reviews:
        user = User.query.get(r.user_id)
        result.append(r.to_dict(include_user_name=user.name if user else "Traveler"))

    avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else 0

    return jsonify({
        "reviews": result,
        "average_rating": avg_rating,
        "total_reviews": len(reviews),
    })


@reviews_bp.route("/destinations/<int:destination_id>", methods=["POST"])
@jwt_required()
def create_review(destination_id):
    """
    Users can leave as many reviews as they like for the same destination --
    no duplicate-check here on purpose, per project requirements.
    """
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    rating = data.get("rating")
    comment = data.get("comment", "").strip()
    trip_id = data.get("trip_id")

    if not rating or not (1 <= int(rating) <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    # Optional: validate the trip belongs to this user if trip_id is provided
    if trip_id:
        trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
        if not trip:
            trip_id = None

    review = Review(
        user_id=user_id,
        destination_id=destination_id,
        trip_id=trip_id,
        rating=int(rating),
        comment=comment,
    )
    db.session.add(review)
    db.session.commit()

    user = User.query.get(user_id)
    return jsonify({"review": review.to_dict(include_user_name=user.name)}), 201


@reviews_bp.route("/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review(review_id):
    user_id = int(get_jwt_identity())
    review = Review.query.filter_by(id=review_id, user_id=user_id).first()
    if not review:
        return jsonify({"error": "Review not found"}), 404

    data = request.get_json() or {}
    if "rating" in data:
        if not (1 <= int(data["rating"]) <= 5):
            return jsonify({"error": "Rating must be between 1 and 5"}), 400
        review.rating = int(data["rating"])
    if "comment" in data:
        review.comment = data["comment"].strip()

    db.session.commit()
    user = User.query.get(user_id)
    return jsonify({"review": review.to_dict(include_user_name=user.name)})


@reviews_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):
    user_id = int(get_jwt_identity())
    review = Review.query.filter_by(id=review_id, user_id=user_id).first()
    if not review:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"})


@reviews_bp.route("/my-reviews", methods=["GET"])
@jwt_required()
def get_my_reviews():
    user_id = int(get_jwt_identity())
    reviews = Review.query.filter_by(user_id=user_id).order_by(Review.created_at.desc()).all()
    return jsonify({"reviews": [r.to_dict() for r in reviews]})