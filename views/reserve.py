from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from config import mydb
import numpy as np


bp = Blueprint('reserve', __name__)

@bp.route('/reserve')
def reserve():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM reservations")
    reserves = cur.fetchall()
    cur.close()
    return render_template('reserve.html', reserves=reserves)

  
@bp.route('/get_room_number', methods=['POST'])
def get_room_number():
    capacity = request.get_json().get('capacity')
    cur = mydb.cursor()
    cur.execute("SELECT room_number FROM rooms WHERE occupancy = 0 AND capacity = %s", (capacity,))
    rn = cur.fetchall()
    session['room_number'] = rn
    return jsonify(rn)

@bp.route('/get_rpn', methods=['POST'])
def get_rpn():
    roomNumber = request.get_json().get('roomNumber')
    cur = mydb.cursor()
    cur.execute("SELECT rate_per_night FROM rooms WHERE room_number = %s", (roomNumber,))
    rpn = cur.fetchall()
    return jsonify(rpn)



@bp.route('/add_reserve', methods=['POST'])
def add_reserve():
  if request.method == 'POST':
    reserve_data = request.get_json()  
    guest_name = reserve_data['guestName']
    phone_number = reserve_data['phoneNumber']
    check_in = reserve_data['checkIn']
    check_out = reserve_data['checkOut']
    number_of_guests = reserve_data['numberOfGuests']
    cur = mydb.cursor()

    roomNumber = session.get('room_number')
    cur.execute("SELECT room_id FROM rooms WHERE room_number = %s", (roomNumber,))
    room_id = cur.fetchone()

    sql_query = "INSERT INTO reservations (guest_name, phone_number, check_in_date, check_out_date, number_of_guests, room_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (guest_name, phone_number, check_in, check_out, number_of_guests, room_id)
    cur.execute(sql_query, values)
    mydb.commit() 
    return redirect(url_for('reserve.reserve'))
  
@bp.route('/delete_reserve', methods=['POST'])
def delete_reserve():
  if request.method == 'POST':
    reserve_data = request.get_json() 
    reserve_id = reserve_data.get('reserveID')
    cur = mydb.cursor()
    sql_query = "DELETE FROM reservations WHERE reservation_id = %s"
    values = (reserve_id),
    cur.execute(sql_query, values)
    mydb.commit() 
    return redirect(url_for('reserve.reserve'))