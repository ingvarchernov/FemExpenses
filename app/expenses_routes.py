# app/expense_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from app.db import get_db_connection

expenses_bp = Blueprint('expenses_bp', __name__)

@expenses_bp.route('/expenses')
def expenses():
    current_app.logger.info('Entered expenses route')
    if 'user_id' not in session:
        return redirect(url_for('user_bp.login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, description, date FROM Expenses")
    expenses = cursor.fetchall()
    cursor.close()
    current_app.logger.debug(f'Fetched expenses for user_id={session["user_id"]}: {expenses}')
    return render_template('expenses.html', expenses=expenses)

@expenses_bp.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('user_bp.login'))
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        date = request.form['date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Expenses (amount, description, date) VALUES (?, ?, ?)",
                       (amount, description, date))
        conn.commit()
        cursor.close()
        conn.close()  # Закриваємо з'єднання після використання
        return redirect(url_for('expenses_bp.expenses'))
    return render_template('add_expense.html')

@expenses_bp.route('/expenses/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        cursor.execute("UPDATE Expenses SET description = ?, amount = ? WHERE id = ?", (description, amount, expense_id))
        conn.commit()
        conn.close()
        return redirect(url_for('expense_bp.expenses'))
    else:
        cursor.execute("SELECT * FROM Expenses WHERE id = ?", (expense_id,))
        expense = cursor.fetchone()
        conn.close()
        return render_template('edit_expenses.html', expense=expense)

@expenses_bp.route('/expenses/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('expense_bp.expenses'))
