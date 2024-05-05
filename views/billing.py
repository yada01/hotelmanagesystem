from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from config import mydb

bp = Blueprint('billing', __name__)

@bp.route('/billing')
def billing():
    cur = mydb.cursor()
    cur.execute("""
        SELECT b.*, r.guest_name, r.phone_number 
        FROM billings b
        JOIN reservations r ON b.reservation_id = r.reservation_id
    """)
    billings = cur.fetchall()
    cur.close()
    return render_template('billing.html', billings=billings)

@bp.route('/get_room_number_billing', methods=['POST'])
def get_room_number_billing():
    phoneNumber = request.get_json().get('phoneNumber')
    cur = mydb.cursor()
    cur.execute("SELECT room_id FROM reservations WHERE phone_number = %s", (phoneNumber,))
    room_id = cur.fetchone()
    cur.close()

    if room_id:
        cur = mydb.cursor()
        cur.execute("SELECT room_number FROM rooms WHERE room_id = %s", (room_id,))
        room_number = cur.fetchone()
        cur.close()
        session['room_id'] = room_id
        return jsonify(room_number)
    else:
        return jsonify({"error": "No room found for the provided phone number"})

@bp.route('/get_total_amount', methods=['POST'])
def get_total_amount():
    room_id = session.get('room_id')
    cur = mydb.cursor()
    cur.execute("SELECT rate_per_night FROM rooms WHERE room_id = %s", (room_id,))
    rpn = cur.fetchone()
    cur.execute("SELECT DATEDIFF(check_in_date, check_out_date) AS days_between FROM reservations WHERE room_id = %s", (room_id))
    numberOfDays = cur.fetchone()
    cur.close()
    return jsonify({'rate_per_night': rpn, 'number_of_days': numberOfDays})

@bp.route('/add_billing', methods=['POST'])
def add_billing():
  if request.method == 'POST':
    billing_data = request.get_json()  
    total_number = billing_data['totalNumber']
    amount_paid = billing_data['amountPaid']
    amount_left = billing_data['amountLeft']
    phone_number = billing_data['phoneNumber']

    cur = mydb.cursor()
    sql_query = "SELECT reservation_id FROM reservations WHERE phone_number = %s"
    cur.execute(sql_query, (phone_number,))
    reservation_id = cur.fetchone()[0]
    cur.close()

    cur = mydb.cursor()
    sql_query = "INSERT INTO billings (total_amount, paid, amount_left, payment_date, reservation_id) VALUES (%s, %s, %s, SYSDATE(), %s)"
    values = (total_number, amount_paid, amount_left, reservation_id)
    cur.execute(sql_query, values)
    mydb.commit()
    cur.close()

    return redirect(url_for('billing.billing'))

@bp.route('/delete_billing', methods=['POST'])
def delete_billing():
  if request.method == 'POST':
    billing_data = request.get_json() 
    billing_id = billing_data.get('billingID')
    cur = mydb.cursor()
    sql_query = "DELETE FROM billings WHERE billing_id = %s"
    values = (billing_id),
    cur.execute(sql_query, values)
    mydb.commit() 
    cur.close()
    return redirect(url_for('billing.billing'))
