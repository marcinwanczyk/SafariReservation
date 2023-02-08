from flask import Blueprint, url_for, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Safari, Ticket, Reservation, User, Guide
from . import db
from sqlalchemy.sql import text, select
import json, datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_id = current_user.id
    reservations = Reservation.query.filter_by(user_id = user_id)
    return render_template("home.html", user=current_user, reservations = reservations)

@views.route('/create-reservation', methods=['POST'])
def create_reservation():
    print("DANE: ", request.form)
    date_str = request.form.get("date_safari")
    date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    safari = Safari.query.filter_by(date=date).first()
    ticket = Ticket(type = request.form.get("package1"), amount = request.form.get("package3"))

    if safari:
        if safari.seats >= int(request.form.get("package3")):
            safari.seats -= int(request.form.get("package3"))
        else:
            flash('No more seats:(', category='error')
            return redirect('/')
    else:
        
        safari = Safari(date = date, type = request.form.get("package2"), users=current_user)
        safari.seats = 20 - int(ticket.amount)
        db.session.add(safari)

    reservation = Reservation(safari=safari, tickets=ticket, users=current_user)
    db.session.add(ticket)
    db.session.add(reservation)
    db.session.commit()   
    return redirect('/')

@views.route('/delete-reservation/<int:id>', methods=['POST'])
def delete_reservation(id):
    reservations = Reservation.query.get(id)

     # musze ogarnac zwracanie zajetych miejsc przy usuwaniu rezerwacji przez danego usera

    # tickets = Ticket.query.get(id)
    #db.session.delete(tickets)
    # db.session.delete(safaris)
    db.session.delete(reservations)
    db.session.commit()
    return redirect('/')

