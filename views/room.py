from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from config import mydb


bp = Blueprint('room', __name__)


@bp.route('/room')
def room():
    cur = mydb.cursor()

    query = """
        SELECT r.room_id, r.check_in_date, r.check_out_date
        FROM reservations r
        WHERE r.check_in_date <= CURDATE()
          AND r.check_out_date >= CURDATE()
    """
    cur.execute(query)
    reserved_rooms = cur.fetchall()

    for room in reserved_rooms:
        room_id = room[0]
        update_query = f"""
            UPDATE rooms
            SET occupancy = 1
            WHERE room_id = {room_id}
        """
        cur.execute(update_query)

    cur.execute("""
        UPDATE rooms
        SET occupancy = 0
        WHERE room_id IN (
            SELECT DISTINCT room_id
            FROM reservations
            WHERE check_out_date < CURDATE()
        )
    """)

    cur.execute("SELECT * FROM rooms")
    rooms = cur.fetchall()
    cur.close()

    return render_template('room.html', rooms=rooms)



@bp.route('/set_housekeeper', methods=['POST'])
def set_housekeeper():
    if request.method == 'POST':
      cur = mydb.cursor()
      room_data = request.get_json()  
      room_number = room_data['roomNumber']
      cur.execute("UPDATE rooms SET housekeeper = (SELECT first_name FROM employees WHERE position = 'Housekeep' AND availability = 0 LIMIT 1) WHERE housekeeper IS NULL;")
      cur.execute("UPDATE employees SET availability = 1 WHERE first_name = (SELECT housekeeper FROM rooms WHERE room_number = %s)", (room_number,))
      mydb.commit() 
      rooms = cur.fetchall()
      cur.close()
      return render_template('room.html', rooms=rooms)



@bp.route('/add_room', methods=['POST'])
def add_room():
  if request.method == 'POST':
    room_data = request.get_json()  
    room_number = room_data['roomNumber']
    room_capacity = room_data['roomCapacity']
    room_rpn = room_data['rpn']
    room_type = room_data['roomType']
    occupancy = room_data['occupancy']
    cur = mydb.cursor()
    sql_query = "INSERT INTO rooms (room_number, capacity, rate_per_night, room_type, occupancy) VALUES (%s, %s, %s, %s, %s)"
    values = (room_number, room_capacity, room_rpn, room_type, occupancy)
    cur.execute(sql_query, values)
    mydb.commit()
  
    return redirect(url_for('room.room'))
  
@bp.route('/delete_room', methods=['POST'])
def delete_room():
  if request.method == 'POST':
    room_data = request.get_json() 
    room_id = room_data.get('roomId')
    cur = mydb.cursor()
    sql_query = "DELETE FROM rooms WHERE room_id = %s"
    values = (room_id),
    cur.execute(sql_query, values)
    mydb.commit() 
    return redirect(url_for('room.room'))
  