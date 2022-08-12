from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from settings import db

class UserInfo(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class MessageHistory(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    username = db.Column(db.String(255))
    message = db.Column(db.String(255))
    datetime = db.Column(db.String(255))

    def __init__(self,username,message,datetime):
        self.username = username
        self.message = message
        self.datetime = datetime
        

db.create_all()