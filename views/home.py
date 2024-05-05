from flask import Blueprint, render_template, request, flash, redirect,url_for
from config import mydb


bp = Blueprint('home', __name__)

@bp.route('/home')
def home():
    return render_template('home.html')