from app import db


class Win(db.Model):
    Win_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    achivement = db.Column(db.String)
    winner = db.Column(db.String)
    # cards = db.relationship("Card", back_populates="board", lazy= True)