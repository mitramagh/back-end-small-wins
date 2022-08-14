from app import db
from flask import jsonify, request
import uuid
import jwt
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps



class Plan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # user = db.relationship("User", back_populates="plans", lazy=True)

    idea = db.Column(db.String)
    planner = db.Column(db.String)    
    contents = db.relationship("Content", back_populates="plan", lazy= True)
    created_date = db.Column (db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

