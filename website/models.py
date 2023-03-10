from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy



class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))
    safari_id = db.Column(db.Integer, db.ForeignKey('safari.id'))
    sum_price = db.Column(db.Integer)
    # date = db.Column(db.DateTime)
    tickets = db.relationship('Ticket')
    users = db.relationship('User')
    #guides = db.relationship('Guide')
    safari = db.relationship('Safari')
    

    

class Safari(db.Model):
    __tablename__ = 'safari'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    type = db.Column(db.String(15000))
    seats = db.Column(db.Integer, nullable = False, default = 20)
    

class Guide(db.Model):
    __tablename__  = 'guide'
    id = db.Column(db.Integer, primary_key=True)
    guide_name = db.Column(db.String(1500))
    surname = db.Column(db.String(1500))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # user_name = db.Column(db.String(150))
    # phone_number = db.Column(db.Integer)
    tickets = db.relationship('Ticket')
    reservation = db.relationship('Reservation')


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key =True)
    price = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    type = db.Column(db.String(150))
    ticket_date = db.Column(db.String(150), db.ForeignKey('safari.date'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('User')

