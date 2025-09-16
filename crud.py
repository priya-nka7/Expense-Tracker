import sqlite3

# Connect to database (or create if it doesn't exist)
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL
)
""")
conn.commit()


def add_expense(data):
    """
    Add a new expense.
    data = {'title': str, 'amount': float/int, 'category': str, 'date': 'YYYY-MM-DD'}
    Returns the new expense id
    """
    cur.execute(
        "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
        (data['title'], float(data['amount']), data['category'], data['date'])
    )
    conn.commit()
    return cur.lastrowid


def get_all_expenses(category=None, date=None):
    """
    Get all expenses optionally filtered by category or date.
    Returns list of dicts with id, title, amount, category, date
    """
    query = "SELECT id, title, amount, category, date FROM expenses"
    params = []

    if category and date:
        query += " WHERE category=? AND date=?"
        params = [category, date]
    elif category:
        query += " WHERE category=?"
        params = [category]
    elif date:
        query += " WHERE date=?"
        params = [date]

    cur.execute(query, params)
    rows = cur.fetchall()
    expenses = []
    for row in rows:
        expenses.append({
            "id": row[0],
            "title": row[1],
            "amount": row[2],
            "category": row[3],
            "date": row[4]
        })
    return expenses


def get_expense_by_id(expense_id):
    cur.execute("SELECT id, title, amount, category, date FROM expenses WHERE id=?", (expense_id,))
    row = cur.fetchone()
    if row:
        return {"id": row[0], "title": row[1], "amount": row[2], "category": row[3], "date": row[4]}
    return None


def delete_expense(expense_id):
    cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    return cur.rowcount > 0  # True if something was deleted

