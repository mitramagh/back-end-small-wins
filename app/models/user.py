from app import db
from flask_login import UserMixin
from flask import jsonify
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    register_at = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    user_name = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    login_id = db.Column(db.Text, nullable=False)

    def response_user_profile(self):
        return {
            "id": self.id,
            "register_at": self.register_at,
            "login_id": self.login_id,
            "email": self.email,
            "name": self.name,
        }

    @staticmethod
    def post_user_oauth(user):
        chosen_user = User.query.get(user["user_id"])
        if not chosen_user:
            new_user = User(
                email=user["email"],
                name=user["name"],
                google_id=user["google_id"],
                user_name=None,
                password=None,
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user), 201

    @staticmethod
    def get_user_oauth(google_id):
        chosen_user = User.query.get(google_id)
        if not chosen_user:
            return None
        return jsonify(chosen_user), 200