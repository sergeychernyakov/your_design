# src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .quiz import Quiz
from .image import Image
