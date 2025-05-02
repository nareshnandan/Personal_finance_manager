from flask import Flask, render_template, request
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        if request.form.get('action') == 'income':
            income_source = request.form['income_source']
            income_amount = request.form['income_amount']
            cursor.execute("INSERT INTO income (source, amount) VALUES (?, ?)", (income_source, income_amount))
        
        elif request.form.get('action') == 'expense':
            expense_category = request.form['expense_category']
            expense_amount = request.form['expense_amount']
            cursor.execute("INSERT INTO expense (category, amount) VALUES (?, ?)", (expense_category, expense_amount))

        conn.commit()
        conn.close()

    incomes, expenses = get_data()
    return render_template('index.html', incomes=incomes, expenses=expenses)

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

    return index()  # Redirect to home page with updated data

if __name__ == '__main__':
    app.run(debug=True)
