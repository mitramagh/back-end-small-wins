from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS , cross_origin
from functools import wraps
import uuid
import jwt
import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']=os.environ.get("JWT_SECRET")
    jwt = JWTManager(app)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.plan import Plan
    from app.models.content import Content
    from app.models.user import User


    from .routes.plan_route import plan_bp
    app.register_blueprint(plan_bp)

    from .routes.content_route import content_bp
    app.register_blueprint(content_bp)

    from .routes.user_route import user_bp
    app.register_blueprint(user_bp)

    CORS(app)
    return app