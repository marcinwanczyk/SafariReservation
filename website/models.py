from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))
    safari_id = db.Column(db.Integer, db.ForeignKey('safari.id'))
    tickets = db.relationship('Ticket')
    users = db.relationship('User')
    guides = db.relationship('Guide')
    safari = db.relationship('Safari')
    

class Safari(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column()
    type = db.Column()
    seats = db.Column()

class Guide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guide_name = db.Column(db.String(150))
    # surname = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    phone_number = db.Column(db.Integer)
    # tickets = db.relationship('Ticket')

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    price = db.Column()
    amount = db.Column()
    type = db.Column()
    ticket_date = db.Column()
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


