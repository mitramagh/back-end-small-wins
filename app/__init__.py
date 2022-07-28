from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.plan import Plan
    from app.models.content import Content


    from .routes.plan_route import plan_bp
    app.register_blueprint(plan_bp)

    from .routes.content_route import content_bp
    app.register_blueprint(content_bp)

    CORS(app)
    return app