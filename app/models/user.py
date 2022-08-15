from app import db, create_app
import uuid
import jwt
from flask_sqlalchemy import SQLAlchemy
import app
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Blueprint, request, jsonify, make_response
from functools import wraps
from flask_login import UserMixin



db = SQLAlchemy()
# def initialize_db(app):
#   app.app_context().push()
#   db.init_app(app)
#   db.create_all()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), unique=False)
    public_id = db.Column(db.Integer)
    # plans = db.relationship("Plan", back_populates="user", lazy= True)

db.create_all(app=create_app())



def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )
def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

def __repr__(self):
        return '<User {}>'.format(self.username)