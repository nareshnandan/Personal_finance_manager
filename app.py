from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM income ORDER BY date DESC")
    incomes = cursor.fetchall()

    cursor.execute("SELECT * FROM expense ORDER BY date DESC")
    expenses = cursor.fetchall()

    conn.close()
    return incomes, expenses

def get_summary(selected_month, selected_year):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Monthly Income
    cursor.execute("SELECT SUM(amount) FROM income WHERE strftime('%Y-%m', date) = ?", (f'{selected_year}-{selected_month:02}',))
    monthly_income = cursor.fetchone()[0] or 0

    # Monthly Expense
    cursor.execute("SELECT SUM(amount) FROM expense WHERE strftime('%Y-%m', date) = ?", (f'{selected_year}-{selected_month:02}',))
    monthly_expense = cursor.fetchone()[0] or 0

    # Yearly Income
    cursor.execute("SELECT SUM(amount) FROM income WHERE strftime('%Y', date) = ?", (selected_year,))
    yearly_income = cursor.fetchone()[0] or 0

    # Yearly Expense
    cursor.execute("SELECT SUM(amount) FROM expense WHERE strftime('%Y', date) = ?", (selected_year,))
    yearly_expense = cursor.fetchone()[0] or 0

    conn.close()

    return {
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_savings': monthly_income - monthly_expense,
        'yearly_income': yearly_income,
        'yearly_expense': yearly_expense,
        'yearly_savings': yearly_income - yearly_expense
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_month = int(request.form.get('month', datetime.now().month))
    selected_year = str(request.form.get('year', datetime.now().year))

    if request.method == 'POST' and request.form.get('action'):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        if request.form['action'] == 'income':
            income_source = request.form['income_source']
            income_amount = request.form['income_amount']
            income_date = request.form['income_date']  # 👈 use date from form
            cursor.execute("INSERT INTO income (source, amount, date) VALUES (?, ?, ?)",
                        (income_source, income_amount, income_date))

        elif request.form['action'] == 'expense':
            expense_category = request.form['expense_category']
            expense_amount = request.form['expense_amount']
            expense_date = request.form['expense_date']  # 👈 use date from form
            cursor.execute("INSERT INTO expense (category, amount, date) VALUES (?, ?, ?)",
                        (expense_category, expense_amount, expense_date))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))



    incomes, expenses = get_data()
    summary = get_summary(selected_month, selected_year)

    return render_template('index.html',
                           incomes=incomes,
                           expenses=expenses,
                           summary=summary,
                           selected_month=selected_month,
                           selected_year=selected_year)

@app.route('/delete', methods=['POST'])
def delete():
    record_type = request.form['type']
    record_id = request.form['id']

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    if record_type == 'income':
        cursor.execute("DELETE FROM income WHERE id = ?", (record_id,))
    elif record_type == 'expense':
        cursor.execute("DELETE FROM expense WHERE id = ?", (record_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
