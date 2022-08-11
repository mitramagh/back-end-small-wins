from email.policy import default
from app import db
from enum import Enum, unique
from sqlalchemy.dialects.postgresql import ENUM as pgEnum

# @unique


# class ContentType(Enum):
#     def __str__(self):
#         return str(self.value)
#     text = 'text'
#     image = 'image'
#     audio = 'audio'
#     video = 'video'


class Content(db.Model):
    content_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # content_type = db.Column(pgEnum(ContentType, name='_option', create_type=False), unique=False, nullable=True)
    content = db.Column(db.String)
    type=db.Column(db.String, nullable=False, default="text")
    like_count = db.Column(db.Integer, default=0)
    comment = db.Column(db.String, nullable=True)
    # color=db.Column(db.String, nullable=True)
    # PosX=db.Column(db.Integer, nullable=True)
    # PosY=db.Column(db.Integer, nullable=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'), nullable=True)
    plan = db.relationship("Plan", back_populates="contents", lazy=True)
    