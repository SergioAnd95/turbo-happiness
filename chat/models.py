from core.db import db


class Room(db.Model):
    __tablename__ = 'chat_rooms'
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(30))
    created_date = db.Column(db.DateTime())


class Message(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Unicode())
    created_date = db.Column(db.DateTime())
    room_id = db.Column(db.Integer(), db.ForeignKey('chat_rooms.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))


class Subscription(db.Model):
    __tablename__ = 'chat_subscriptions'
    
    room_id = db.Column(db.Integer(), db.ForeignKey('chat_rooms.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))