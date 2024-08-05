# src/models/image.py

from flask_sqlalchemy import SQLAlchemy
from . import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.String, db.ForeignKey('quiz.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_path = db.Column(db.String(256))
    phone_number = db.Column(db.String(16))
