from flask import Flask, render_template, request

from database import add_expense_to_db, add_user_to_db, dashboard, dashboard_by_month, delete_expense, edit_expense, load_catagories, load_expenses, load_user_details, load_users


app = Flask(__name__)

@app.route('/')

def home():
    dashboard_data_by_month = dashboard_by_month()
    
    dashboard_data = dashboard()
    categories = [row['category_name'] for row in dashboard_data]
    total_amounts = [row['total_amount'] for row in dashboard_data]
    months = [row['month'] for row in dashboard_data_by_month]
    amount_by_month = [row['total_amount'] for row in dashboard_data_by_month]
    return render_template('Home.html', categories=categories, total_amounts=total_amounts , month=months, amount_by_month=amount_by_month)

@app.route('/add_user',methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_data=request.form
        add_user_to_db(user_data['username'], user_data['email'])
        return render_template('add_user.html')
    return render_template('add_user.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    expense_data = request.form
    categories = load_catagories()
    users = load_users()
    if request.method == 'POST':
        add_expense_to_db(expense_data['expenseName'], expense_data['expenseUser'], expense_data['expenseCategory'], expense_data['expenseAmount'], expense_data['expenseDate'])
        return render_template('add_expense.html', message="Expense added successfully", cat=categories, users=users)
    return render_template('add_expense.html', cat=categories, users=users)



@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])

def edit_expense_page(expense_id):
    categories = load_catagories()
    users = load_users()
   
    all_expenses = load_expenses()
    expense = next((e for e in all_expenses if e['id'] == expense_id), None)
    if request.method == 'POST':
        expense_data = request.form
        edit_expense(
            expense_id,
            expense_data['expenseName'],
            expense_data['expenseUser'],
            expense_data['expenseCategory'],
            expense_data['expenseAmount'],
            expense_data['expenseDate']
        )        
        all_expenses = load_expenses()
        expense = next((e for e in all_expenses if e['id'] == expense_id), None)
        return render_template('edit_expense.html', message="Expense updated successfully", cat=categories, users=users, expense=expense)
    return render_template('edit_expense.html', cat=categories, users=users, expense=expense)

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense_page(expense_id):    
    delete_expense(expense_id)
    return render_template('Home.html', message="Expense deleted successfully")

@app.route('/view_expenses')
def view_expenses():
    expenses = load_expenses()
    categories = load_catagories()
    users = load_users()
    user_map = {user['id']: user['name'] for user in users}
    return render_template('view_expenses.html', expenses=expenses, categories=categories, users=user_map)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")