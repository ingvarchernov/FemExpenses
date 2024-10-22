# app/user_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db_connection

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

@user_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        role = request.form['role']

        cursor.execute("""
            UPDATE Users
            SET username = ?, name = ?, surname = ?, email = ?, role = ?
            WHERE id = ?
        """, (username, name, surname, email, role, user_id))
        conn.commit()
        cursor.close()
        return redirect(url_for('user_bp.user_list'))

    cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    return render_template('edit_user.html', user=user)


@user_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('user_bp.users'))


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    current_app.logger.info('Entered register route')

    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        current_app.logger.debug(f'Registration data: username={username}, name={name}, surname={surname}, email={email}, role={role}')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Перевірка на пусту таблицю (чи є користувачі в БД)
        cursor.execute("SELECT COUNT(*) FROM Users")
        # Отримання кількості користувачів
        result = cursor.fetchone()
        if result is not None:
            # Якщо є користувачі, перевірка на унікальність username та email
            cursor.execute("SELECT * FROM Users WHERE username = %s OR email = %s", (username, email))
            user = cursor.fetchone()

            if user:
                flash('Username or email already exists', 'danger')
                current_app.logger.debug(f'User with username {username} or email {email} already exists.')
                return redirect(url_for('user_bp.register'))

            # Додавання нового користувача, якщо немає дубля
            cursor.execute("INSERT INTO Users (username, name, surname, email, password, role) VALUES (%s, %s, %s, %s, %s, %s)",
                        (username, name, surname, email, hashed_password, role))
            conn.commit()
            cursor.close()

            flash('Registration successful!', 'success')
            return redirect(url_for('user_bp.login'))
        else:
            current_app.logger.info('No users found in the database. Registering the first user.')
            # Якщо немає користувачів, реєструємо першого
            cursor.execute("INSERT INTO Users (username, name, surname, email, password, role) VALUES (%s, %s, %s, %s, %s, %s)",
                           (username, name, surname, email, hashed_password, role))
            conn.commit()
            cursor.close()

            flash('First user registered successfully!', 'success')
            return redirect(url_for('user_bp.login')) # Обробка випадку, коли немає користувачів

    return render_template('register_user.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info('Entered login route')
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        current_app.logger.debug(f'Login attempt with: username_or_email={username_or_email}')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = %s OR email = %s", (username_or_email, username_or_email))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('main_bp.index'))
        else:
            flash('Invalid username/email or password', 'danger')
            return redirect(url_for('user_bp.login'))
    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user_bp.login'))

