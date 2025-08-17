from sqlalchemy import create_engine, Column, Integer, String, Float, Date, text
import os
from dotenv import load_dotenv


load_dotenv()

engine= create_engine(os.getenv("DB_connection_string"))

def load_catagories():
    with engine.connect() as conn:
        result= conn.execute(text("SELECT * FROM catagories"))
        categories=result.mappings().all()
        print("Categories loaded successfully")
        print(categories[0])
        return categories

def add_user_to_db(name, email):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO users (name, email) VALUES (:name, :email)"),
                     {"name": name, "email": email})        
        conn.commit()

def load_users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        users = result.mappings().all()
        print("Users loaded successfully", users)
        return users
    
def add_expense_to_db(title, user_id, catagory_id, amount, expense_date):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO expenses (title, user_id, catagory_id, amount, expense_date) VALUES (:title, :user_id, :catagory_id, :amount, :expense_date)"),
                     {"title": title, "user_id": user_id, "catagory_id": catagory_id, "amount": amount, "expense_date": expense_date})
        conn.commit()

def load_expenses():
    with engine.connect () as conn:
        result = conn.execute(text("SELECT * FROM expenses"))
        expenses = result.mappings().all()
        print("Expenses loaded successfully")
        return expenses
    
def load_user_details(user_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :user_id"), {"user_id": user_id})
        user_details = result.mappings().all()
        print("User details loaded successfully")
        return user_details
    

def dashboard():
    with engine.connect() as conn:
        result= conn.execute(text("""
            SELECT c.name AS category_name,
                   SUM(e.amount) AS total_amount
            FROM expenses e
            JOIN catagories c ON e.catagory_id = c.id
            
            GROUP BY c.name
        """),)
        dashboard_data = result.mappings().all()
        print("Dashboard data loaded successfully")
        return dashboard_data
    
def dashboard_by_month():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT DATE_FORMAT(e.expense_date, '%Y-%m') AS month,
                   SUM(e.amount) AS total_amount
            FROM expenses e
            GROUP BY month
        """))
        monthly_data = result.mappings().all()
        print("Monthly dashboard data loaded successfully")
        return monthly_data
    
def edit_expense(expense_id, title, user_id, catagory_id, amount, expense_date):
    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE expenses
            SET title = :title,
                user_id = :user_id,
                catagory_id = :catagory_id,
                amount = :amount,
                expense_date = :expense_date
            WHERE id = :expense_id
        """), {
            "title": title,
            "user_id": user_id,
            "catagory_id": catagory_id,
            "amount": amount,
            "expense_date": expense_date,
            "expense_id": expense_id
        })
        conn.commit()

def delete_expense(expense_id):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM expenses WHERE id = :expense_id"), {"expense_id": expense_id})
        conn.commit()
        print(f"Expense with ID {expense_id} deleted successfully")