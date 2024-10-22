# app/expense_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from app.db import get_db_connection

expenses_bp = Blueprint('expenses_bp', __name__)

@expenses_bp.route('/expenses')
def expenses():
    current_app.logger.info('Entered expenses route')
    if 'user_id' not in session:
        return redirect(url_for('user_bp.login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, description, expenses_date FROM Expenses")
    expenses = cursor.fetchall()
    cursor.close()
    current_app.logger.debug(f'Fetched expenses for user_id={session["user_id"]}: {expenses}')
    return render_template('expenses.html', expenses=expenses)

@expenses_bp.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['expenses_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Expenses (description, amount, expenses_date)
            VALUES (?, ?, ?)
        """, (description, amount, date))
        conn.commit()
        cursor.close()

        return redirect(url_for('expenses_bp.expenses'))
    return render_template('add_expenses.html')

@expenses_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['expenses_date']

        cursor.execute("""
            UPDATE Expenses
            SET description = ?, amount = ?, date = ?
            WHERE id = ?
        """, (description, amount, date, id))
        conn.commit()
        cursor.close()

        return redirect(url_for('expenses_bp.expenses'))

    cursor.execute("SELECT * FROM Expenses WHERE id = ?", (id,))
    expense = cursor.fetchone()
    cursor.close()

    return render_template('edit_expenses.html', expense=expense)

@expenses_bp.route('/delete/<int:id>')
def delete_expense(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Expenses WHERE id = ?", (id,))
    conn.commit()
    cursor.close()

    return redirect(url_for('expenses_bp.expenses'))
