from app import db
import enum

class ContentType(enum.Enum):
    TEXT = "Text"
    IMAGELINK = "ImageLink"
    AUDIOLINK = "AudioLink"
    VIDEOLINK = "VideoLink"


class Content(db.Model):
    content_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content_type = db.Column(db.Enum(ContentType))
    content = db.Column(db.String)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'), nullable=True)
    plan = db.relationship("Plan", back_populates="contents", lazy= True)
    like_count = db.Column(db.Integer, default=0)
    comment = db.Column(db.String, nullable=True)

