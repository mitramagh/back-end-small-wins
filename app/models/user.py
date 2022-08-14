from app import db
import uuid
import jwt
from flask_sqlalchemy import SQLAlchemy
import app
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Blueprint, request, jsonify, make_response
from functools import wraps



db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), unique=False)
    public_id = db.Column(db.Integer)
    # plans = db.relationship("Plan", back_populates="user", lazy= True)


# db.create_all()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator