from app import db


class Plan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idea = db.Column(db.String)
    planner = db.Column(db.String)    