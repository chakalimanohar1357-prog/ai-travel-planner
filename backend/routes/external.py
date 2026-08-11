import requests
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required

external_bp = Blueprint("external", __name__, url_prefix="/api/external")


@external_bp.route("/weather", methods=["GET"])
@jwt_required()
def weather():
    """
    Fetches current weather + short forecast from OpenWeatherMap.
    Requires OPENWEATHER_API_KEY in .env. Falls back to a mock response
    if no key is configured, so the app remains demoable offline.
    """
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    city = request.args.get("city")
    api_key = current_app.config.get("OPENWEATHER_API_KEY")

    if not api_key:
        return jsonify({
            "mock": True,
            "message": "OPENWEATHER_API_KEY not configured - showing sample data.",
            "city": city or "Sample City",
            "temperature_c": 27,
            "condition": "Partly Cloudy",
            "humidity": 65,
            "forecast": [
                {"day": "Day 1", "temp_c": 27, "condition": "Sunny"},
                {"day": "Day 2", "temp_c": 25, "condition": "Partly Cloudy"},
                {"day": "Day 3", "temp_c": 24, "condition": "Light Rain"},
            ],
        })

    try:
        params = {"appid": api_key, "units": "metric"}
        if city:
            params["q"] = city
        elif lat and lon:
            params.update({"lat": lat, "lon": lon})
        else:
            return jsonify({"error": "city or lat/lon required"}), 400

        resp = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return jsonify({
            "mock": False,
            "city": data.get("name"),
            "temperature_c": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
        })
    except requests.RequestException as e:
        return jsonify({"error": f"Weather service unavailable: {e}"}), 502


@external_bp.route("/places", methods=["GET"])
@jwt_required()
def places():
    """
    Fetches nearby places using Google Places API (Nearby Search).
    Requires GOOGLE_PLACES_API_KEY. Falls back to mock data if unset.
    """
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    place_type = request.args.get("type", "tourist_attraction")
    api_key = current_app.config.get("GOOGLE_PLACES_API_KEY")

    if not api_key or not lat or not lon:
        return jsonify({
            "mock": True,
            "message": "GOOGLE_PLACES_API_KEY not configured or lat/lon missing - showing sample data.",
            "places": [
                {"name": "Sample Landmark", "rating": 4.6, "type": place_type},
                {"name": "Local Market", "rating": 4.3, "type": place_type},
                {"name": "Scenic Viewpoint", "rating": 4.8, "type": place_type},
            ],
        })

    try:
        params = {
            "location": f"{lat},{lon}",
            "radius": 5000,
            "type": place_type,
            "key": api_key,
        }
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params=params, timeout=10,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        places_list = [
            {"name": p.get("name"), "rating": p.get("rating"), "vicinity": p.get("vicinity")}
            for p in results[:10]
        ]
        return jsonify({"mock": False, "places": places_list})
    except requests.RequestException as e:
        return jsonify({"error": f"Places service unavailable: {e}"}), 502


@external_bp.route("/directions", methods=["GET"])
@jwt_required()
def directions():
    """
    Route optimization via Google Directions API (origin -> destination,
    with optional waypoints for multi-stop day plans).
    """
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    waypoints = request.args.get("waypoints", "")
    api_key = current_app.config.get("GOOGLE_MAPS_API_KEY")

    if not api_key or not origin or not destination:
        return jsonify({
            "mock": True,
            "message": "GOOGLE_MAPS_API_KEY not configured or origin/destination missing - showing sample data.",
            "distance_km": 12.4,
            "duration_minutes": 28,
            "optimized_order": waypoints.split("|") if waypoints else [],
        })

    try:
        params = {
            "origin": origin, "destination": destination,
            "key": api_key, "optimize": "true",
        }
        if waypoints:
            params["waypoints"] = f"optimize:true|{waypoints}"

        resp = requests.get("https://maps.googleapis.com/maps/api/directions/json", params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("routes"):
            return jsonify({"error": "No route found"}), 404

        leg = data["routes"][0]["legs"][0]
        return jsonify({
            "mock": False,
            "distance": leg["distance"]["text"],
            "duration": leg["duration"]["text"],
            "optimized_waypoint_order": data["routes"][0].get("waypoint_order", []),
        })
    except requests.RequestException as e:
        return jsonify({"error": f"Directions service unavailable: {e}"}), 502
