from flask import Flask, render_template, request

app = Flask(__name__)

# Dummy lists to store data temporarily (later we’ll save to file or DB)
income_list = []
expense_list = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'income':
            source = request.form.get('income_source')
            amount = request.form.get('income_amount')
            income_list.append({'source': source, 'amount': float(amount)})

        elif action == 'expense':
            category = request.form.get('expense_category')
            amount = request.form.get('expense_amount')
            expense_list.append({'category': category, 'amount': float(amount)})

    return render_template("index.html", income=income_list, expenses=expense_list)

if __name__ == '__main__':
    app.run(debug=True)
