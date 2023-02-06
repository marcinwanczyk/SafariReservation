from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Safari, Ticket, Reservation
from . import db
import json, datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# @views.route('/create_safari', methods=['POST'])
# def create_safari():
#     date_str = request.form['date_safari']
#     date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
#     safari = Safari(date=date, type=request.form['type'], seats=request.form['seats'])
#     db.session.add(safari)
#     db.session.commit()
#     return render_template("home.html", user=current_user)


@views.route('/create-reservation', methods=['POST'])
def create_reservation():
    date_str = request.form['date_safari']
    date = datetime.strptime(date_str, '%d-%m-%YT%H:%M')
    safari= Safari(date = date, type = request.form['package2'])
    ticket = Ticket(type = request.form['package1'], amount = request.form['package3'],
     user_id=current_user.id)
    reservation = Reservation(date = date )
    db.session.add(safari)
    db.session.add(ticket)
    db.session.add(reservation)
    db.session.commit
    return render_template("home.html", user=current_user)
# nie postuje wciaz

