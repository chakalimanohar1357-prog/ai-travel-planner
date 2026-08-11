from flask import Blueprint, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import Destination, BlockedDestination

destinations_bp = Blueprint("destinations", __name__, url_prefix="/api/destinations")


@destinations_bp.route("", methods=["GET"])
def list_destinations():
    """
    Public endpoint -- works for logged-out visitors too. If a valid JWT is
    present, destinations the user has blocked in Settings are filtered out.
    """
    blocked_ids = set()
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            blocked_ids = {
                b.destination_id
                for b in BlockedDestination.query.filter_by(user_id=int(identity)).all()
            }
    except Exception:
        pass

    destinations = Destination.query.all()
    return jsonify({
        "destinations": [d.to_dict() for d in destinations if d.id not in blocked_ids]
    })


@destinations_bp.route("/<int:destination_id>", methods=["GET"])
def get_destination(destination_id):
    dest = Destination.query.get(destination_id)
    if not dest:
        return jsonify({"error": "Destination not found"}), 404
    return jsonify({"destination": dest.to_dict()})