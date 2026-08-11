import requests
from flask import Blueprint, jsonify, current_app

currency_bp = Blueprint("currency", __name__, url_prefix="/api/currency")

FALLBACK_RATES = {
    "USD": 1.0,
    "INR": 83.5,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 156.0,
    "AUD": 1.51,
    "CAD": 1.36,
    "SGD": 1.34,
    "AED": 3.67,
}


@currency_bp.route("/rates", methods=["GET"])
def get_rates():
    api_key = current_app.config.get("EXCHANGE_RATE_API_KEY")

    if not api_key:
        return jsonify({
            "mock": True,
            "base": "USD",
            "message": "EXCHANGE_RATE_API_KEY not configured - showing approximate sample rates.",
            "rates": FALLBACK_RATES,
        })

    try:
        resp = requests.get(
            f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD", timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("result") != "success":
            raise ValueError(data.get("error-type", "unknown error"))

        rates = {cur: data["conversion_rates"][cur] for cur in FALLBACK_RATES if cur in data["conversion_rates"]}
        return jsonify({"mock": False, "base": "USD", "rates": rates})
    except (requests.RequestException, ValueError, KeyError) as e:
        return jsonify({
            "mock": True,
            "base": "USD",
            "message": f"Live rate service unavailable ({e}) - showing approximate sample rates.",
            "rates": FALLBACK_RATES,
        })