from flask import Blueprint, render_template, redirect, url_for, session
from app.db import get_db_connection

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('user_bp.login'))
    return render_template('index.html')

@main_bp.route('/users')
def users():
    if 'user_id' not in session:
        return redirect(url_for('user_bp.login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, name, surname, email, role FROM Users")
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users)
