import os
from flask import Flask, jsonify
from config import Config
from extensions import db, bcrypt, jwt, cors
from routes.settings import settings_bp
from routes.bookings import bookings_bp
from routes.currency import currency_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    from routes.auth import auth_bp
    from routes.trips import trips_bp
    from routes.recommendations import recommendations_bp
    from routes.chatbot import chatbot_bp
    from routes.external import external_bp
    from routes.admin import admin_bp
    from routes.destinations import destinations_bp
    from routes.review import reviews_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(currency_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(external_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(destinations_bp)
    app.register_blueprint(reviews_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "AI Travel Planner API"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)