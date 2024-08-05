# src/models/user.py

from flask_sqlalchemy import SQLAlchemy
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(16))
    images = db.relationship('Image', backref='user', lazy=True)
