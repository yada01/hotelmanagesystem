from flask import Blueprint, render_template, request, flash, redirect,url_for
from config import mydb


bp = Blueprint('employee', __name__)

@bp.route('/employee', methods=['GET', 'POST'])
def employee():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    return render_template('employee.html', employees=employees)

@bp.route('/add_employee', methods=['POST'])
def add_employee():
  if request.method == 'POST':
    employee_data = request.get_json()  
    first_name = employee_data['firstName']
    last_name = employee_data['lastName']
    position = employee_data['position']
    salary = employee_data['salary']
    cur = mydb.cursor()
    sql_query = "INSERT INTO employees (first_name, last_name, position, salary, availability) VALUES (%s, %s, %s, %s, 0)"
    values = (first_name, last_name, position, salary)
    cur.execute(sql_query, values)
    mydb.commit() 
    return redirect(url_for('employee.employee'))
  
@bp.route('/delete_employee', methods=['POST'])
def delete_employee():
  if request.method == 'POST':
    employee_data = request.get_json() 
    staff_id = employee_data.get('staffId')
    cur = mydb.cursor()
    sql_query = "DELETE FROM employees WHERE staff_id = %s"
    values = (staff_id,)
    cur.execute(sql_query, values)
    mydb.commit() 
    return redirect(url_for('employee.employee'))