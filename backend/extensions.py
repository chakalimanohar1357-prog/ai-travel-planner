from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    from models import Session
    jti = jwt_payload["jti"]
    session = Session.query.filter_by(jti=jti).first()
    return session.revoked if session else False
cors = CORS()
