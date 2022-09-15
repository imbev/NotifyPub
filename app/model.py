from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

@dataclass
class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)
    feed = db.relationship('Feed')

@dataclass
class Feed(db.Model):
    __tablename__ = 'feed'
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', back_populates='feed')

@dataclass
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    feed = db.relationship('Feed', back_populates='message')