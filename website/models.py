from enum import Enum, unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#accountType = ('teacher', 'student')

class Room(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    halaqa_code = db.Column(db.String(6), unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    recording = db.relationship('Recording')

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(150), unique=True)
    room = db.Column(db.String(6), db.ForeignKey('room.id'))
    student = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    account_type = db.Column(db.String(150), nullable=False)
    rooms = db.relationship("Room")
