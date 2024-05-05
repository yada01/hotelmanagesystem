from flask import Blueprint, render_template, request, flash, redirect,url_for
from config import mydb


bp = Blueprint('login', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mydb.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password,))
        account = cur.fetchone()
        if account:
            return redirect(url_for('home.home'))
        else:
            flash('Invalid login credentials')
    return render_template('login.html')