# src/models/quiz.py

from flask_sqlalchemy import SQLAlchemy
from . import db

class Quiz(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(128))
    created = db.Column(db.String(32))
    images = db.relationship('Image', backref='quiz', lazy=True)
