import random
import time
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Booking, Trip, Destination, generate_reference

bookings_bp = Blueprint("bookings", __name__, url_prefix="/api/bookings")


@bookings_bp.route("", methods=["POST"])
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    trip_id = data.get("trip_id")
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first() if trip_id else None

    booking = Booking(
        user_id=user_id,
        trip_id=trip.id if trip else None,
        destination_id=trip.destination_id if trip else data.get("destination_id"),
        booking_type=data.get("booking_type", "full_trip"),
        item_name=trip.destination_name if trip else data.get("item_name", "Trip"),
        travelers=trip.travelers if trip else data.get("travelers", 1),
        amount=trip.estimated_cost if trip else float(data.get("amount", 0)),
        currency=data.get("currency", "USD"),
        payment_status="pending",
        booking_reference=generate_reference("BK"),
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify({"booking": booking.to_dict()}), 201


@bookings_bp.route("/<int:booking_id>/pay", methods=["POST"])
@jwt_required()
def pay_booking(booking_id):
    user_id = int(get_jwt_identity())
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking.payment_status == "success":
        return jsonify({"error": "This booking has already been paid for"}), 409

    data = request.get_json() or {}
    payment_method = data.get("payment_method", "card")
    card_number = data.get("card_number", "").replace(" ", "")

    time.sleep(1)

    simulated_failure = payment_method == "card" and card_number.endswith("0000") and len(card_number) >= 4

    if simulated_failure:
        booking.payment_status = "failed"
        db.session.commit()
        return jsonify({
            "booking": booking.to_dict(),
            "message": "Payment declined by simulated gateway. Try a different card number.",
        }), 402

    booking.payment_method = payment_method
    booking.payment_status = "success"
    booking.transaction_id = "TXN" + "".join(random.choices("0123456789", k=12))
    if payment_method == "card" and card_number:
        booking.card_last4 = card_number[-4:]

    db.session.commit()

    return jsonify({
        "booking": booking.to_dict(),
        "message": "Payment successful!",
    })


@bookings_bp.route("", methods=["GET"])
@jwt_required()
def get_my_bookings():
    user_id = int(get_jwt_identity())
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
    return jsonify({"bookings": [b.to_dict() for b in bookings]})


@bookings_bp.route("/<int:booking_id>", methods=["GET"])
@jwt_required()
def get_booking(booking_id):
    user_id = int(get_jwt_identity())
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify({"booking": booking.to_dict()})


@bookings_bp.route("/<int:booking_id>", methods=["DELETE"])
@jwt_required()
def cancel_booking(booking_id):
    user_id = int(get_jwt_identity())
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking cancelled"})