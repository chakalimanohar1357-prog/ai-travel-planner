import random
import string
from datetime import datetime
from extensions import db


def generate_reference(prefix="BK"):
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}-{suffix}"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")  # user | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trips = db.relationship("Trip", backref="user", cascade="all, delete-orphan")
    favorites = db.relationship("Favorite", backref="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }


class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    tags = db.Column(db.String(255))  # comma separated: adventure,beaches,history...
    avg_daily_cost = db.Column(db.Float, default=50.0)  # in USD
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    popularity_score = db.Column(db.Float, default=0.5)
    image_url = db.Column(db.String(255), default="")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "description": self.description,
            "tags": self.tags.split(",") if self.tags else [],
            "avg_daily_cost": self.avg_daily_cost,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "popularity_score": self.popularity_score,
            "image_url": self.image_url,
        }


class Hotel(db.Model):
    __tablename__ = "hotels"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))
    name = db.Column(db.String(120), nullable=False)
    price_per_night = db.Column(db.Float, default=50.0)
    rating = db.Column(db.Float, default=4.0)
    category = db.Column(db.String(50), default="mid-range")
    amenities = db.Column(db.String(255), default="")
    image_url = db.Column(db.String(500), default="")
    address = db.Column(db.String(255), default="")
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "name": self.name,
            "price_per_night": self.price_per_night,
            "rating": self.rating,
            "category": self.category,
            "amenities": self.amenities.split(",") if self.amenities else [],
            "image_url": self.image_url,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))
    name = db.Column(db.String(120), nullable=False)
    cuisine = db.Column(db.String(120), default="")
    avg_cost = db.Column(db.Float, default=15.0)
    rating = db.Column(db.Float, default=4.0)
    image_url = db.Column(db.String(500), default="")
    address = db.Column(db.String(255), default="")
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "name": self.name,
            "cuisine": self.cuisine,
            "avg_cost": self.avg_cost,
            "rating": self.rating,
            "image_url": self.image_url,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


class Attraction(db.Model):
    __tablename__ = "attractions"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), default="sightseeing")
    est_duration_hours = db.Column(db.Float, default=2.0)
    entry_fee = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float, default=4.0)
    image_url = db.Column(db.String(500), default="")
    address = db.Column(db.String(255), default="")
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "name": self.name,
            "category": self.category,
            "est_duration_hours": self.est_duration_hours,
            "entry_fee": self.entry_fee,
            "rating": self.rating,
            "image_url": self.image_url,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))
    destination_name = db.Column(db.String(120))
    budget = db.Column(db.Float, default=0.0)
    duration_days = db.Column(db.Integer, default=1)
    travelers = db.Column(db.Integer, default=1)
    interests = db.Column(db.String(255), default="")
    transport_mode = db.Column(db.String(50), default="flight")
    accommodation_pref = db.Column(db.String(50), default="mid-range")
    itinerary_json = db.Column(db.Text)  # generated day-wise plan, stored as JSON string
    estimated_cost = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default="planned")  # planned | ongoing | completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "user_id": self.user_id,
            "destination_id": self.destination_id,
            "destination_name": self.destination_name,
            "budget": self.budget,
            "duration_days": self.duration_days,
            "travelers": self.travelers,
            "interests": self.interests.split(",") if self.interests else [],
            "transport_mode": self.transport_mode,
            "accommodation_pref": self.accommodation_pref,
            "itinerary": json.loads(self.itinerary_json) if self.itinerary_json else [],
            "estimated_cost": self.estimated_cost,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    comment = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_user_name=None):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": include_user_name,
            "destination_id": self.destination_id,
            "trip_id": self.trip_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat(),
        }


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"), nullable=True)

    booking_type = db.Column(db.String(30), default="full_trip")  # full_trip | hotel | attraction
    item_name = db.Column(db.String(150), default="")
    travelers = db.Column(db.Integer, default=1)
    amount = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default="USD")

    payment_method = db.Column(db.String(30), default="card")  # card | upi | paypal
    payment_status = db.Column(db.String(20), default="pending")  # pending | success | failed
    transaction_id = db.Column(db.String(50), unique=True)

    card_last4 = db.Column(db.String(4), default="")
    booking_reference = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "trip_id": self.trip_id,
            "destination_id": self.destination_id,
            "booking_type": self.booking_type,
            "item_name": self.item_name,
            "travelers": self.travelers,
            "amount": self.amount,
            "currency": self.currency,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "transaction_id": self.transaction_id,
            "card_last4": self.card_last4,
            "booking_reference": self.booking_reference,
            "created_at": self.created_at.isoformat(),
        }


class UserSettings(db.Model):
    __tablename__ = "user_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    currency = db.Column(db.String(10), default="USD")
    language = db.Column(db.String(10), default="en")  # en | hi

    default_budget = db.Column(db.Float, default=1000.0)
    default_duration_days = db.Column(db.Integer, default=5)
    default_interests = db.Column(db.String(255), default="")

    email_notifications = db.Column(db.Boolean, default=True)
    profile_photo_url = db.Column(db.String(500), default="")

    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_pin_hash = db.Column(db.String(255), default="")

    unit_system = db.Column(db.String(10), default="metric")  # metric | imperial
    home_city = db.Column(db.String(120), default="")
    emergency_contact_name = db.Column(db.String(120), default="")
    emergency_contact_phone = db.Column(db.String(30), default="")
    map_style = db.Column(db.String(20), default="roadmap")  # roadmap | satellite | terrain
    font_size = db.Column(db.String(10), default="normal")  # normal | large
    high_contrast = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "currency": self.currency,
            "language": self.language,
            "default_budget": self.default_budget,
            "default_duration_days": self.default_duration_days,
            "default_interests": self.default_interests.split(",") if self.default_interests else [],
            "email_notifications": self.email_notifications,
            "profile_photo_url": self.profile_photo_url,
            "two_factor_enabled": self.two_factor_enabled,
            "unit_system": self.unit_system,
            "home_city": self.home_city,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
            "map_style": self.map_style,
            "font_size": self.font_size,
            "high_contrast": self.high_contrast,
        }


class LoginActivity(db.Model):
    __tablename__ = "login_activity"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ip_address = db.Column(db.String(64), default="")
    user_agent = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat(),
        }


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    jti = db.Column(db.String(64), unique=True, nullable=False)
    device_info = db.Column(db.String(255), default="")
    ip_address = db.Column(db.String(64), default="")
    revoked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "device_info": self.device_info,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat(),
        }


class BlockedDestination(db.Model):
    __tablename__ = "blocked_destinations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    name = db.Column(db.String(120), default="")
    email = db.Column(db.String(120), default="")
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "destination_id": self.destination_id,
            "created_at": self.created_at.isoformat(),
        }