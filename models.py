from flask_login import UserMixin
from app import db

##database objects below

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(200), nullable = False)
    email=db.Column(db.String(101), nullable = False, unique = True)
    password=db.Column(db.String(80), nullable = False)