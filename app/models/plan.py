from app import db
from datetime import datetime


class Plan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idea = db.Column(db.String)
    planner = db.Column(db.String)    
    contents = db.relationship("Content", back_populates="plan", lazy= True)
    # created_date = db.Column (db.DateTime, nullable=False, default=datetime.utcnow)