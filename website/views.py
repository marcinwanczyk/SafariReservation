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
    type = request.form.get("package2")
    safari = Safari.query.filter_by(date=date, type=type).first()

    ticket_type = request.form.get("package1")

    if ticket_type == "full":
        price = 100
    elif ticket_type == "reduced":
        price = 50
    

    ticket = Ticket(type = ticket_type , amount = request.form.get("package3"),
                    ticket_date = date, users = current_user, price = int(price))

    if safari:
        if safari.seats >= int(request.form.get("package3")):
            safari.seats -= int(request.form.get("package3"))
        
        elif safari.seats < int(request.form.get("package3")) and safari.seats > 1:
            flash('There is only ' + str(safari.seats) +' seats left', category='error')
            return redirect('/')
        
        elif safari.seats == 1:
            flash('There is only ' + str(safari.seats) +' seat left', category='error')
            return redirect('/')
      
        else:
            flash('No more seats left:(', category='error')
            return redirect('/')
    else:
        
        safari = Safari(date = date, type = request.form.get("package2"))
        safari.seats = 20 - int(ticket.amount)
        db.session.add(safari)

    reservation = Reservation(safari=safari, tickets=ticket, users=current_user, sum_price = (int(ticket.amount) * int(ticket.price)))
    db.session.add(ticket)
    db.session.add(reservation)
    db.session.commit()   
    return redirect('/')

@views.route('/delete-reservation/<int:id>', methods=['POST'])
def delete_reservation(id):
    reservations = Reservation.query.get(id)
    safari = reservations.safari
    safari.seats += reservations.tickets.amount
    tickets = reservations.tickets
    db.session.delete(tickets)
    db.session.delete(reservations)
    db.session.commit()
    return redirect('/')

@views.route('/admin', methods=['GET', 'POST'])
def admin():
    reservations = Reservation.query.all()
    user_id = current_user.id
    return render_template('admin.html',user = current_user, reservations=reservations)

