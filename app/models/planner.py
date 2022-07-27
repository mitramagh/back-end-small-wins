from app import db


class Planner(db.Model):
    planner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey ('plan.plan_id'), nullable=True)
    plan = db.relationship("Plan", back_populates="plan", lazy= True)