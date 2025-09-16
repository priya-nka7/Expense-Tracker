from flask import Flask, request, jsonify
import crud
import datetime
from collections import defaultdict

app = Flask(__name__, static_folder="frontend", static_url_path="")

# Serve frontend index.html
@app.route("/")
def index():
    return app.send_static_file("index.html")

# Create expense
@app.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json() or {}
    # basic validation
    for field in ("title", "amount", "category", "date"):
        if field not in data or data[field] == "":
            return jsonify({"error": f"{field} is required"}), 400
    try:
        data['amount'] = float(data['amount'])
    except ValueError:
        return jsonify({"error": "amount must be a number"}), 400

    expense_id = crud.add_expense(data)
    return jsonify({"message": "Expense added", "id": expense_id}), 201

# List expenses (optional query: ?category=Food or ?date=2025-09-16)
@app.route("/expenses", methods=["GET"])
def list_expenses():
    category = request.args.get("category")
    date = request.args.get("date")
    expenses = crud.get_all_expenses(category=category, date=date)
    return jsonify({"expenses": expenses})

# Get single expense
@app.route("/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    exp = crud.get_expense_by_id(expense_id)
    if not exp:
        return jsonify({"error": "Expense not found"}), 404
    return jsonify(exp)

# Delete expense
@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    deleted = crud.delete_expense(expense_id)
    if deleted:
        return jsonify({"message": "Expense deleted"})
    return jsonify({"error": "Expense not found"}), 404

# grouped endpoint
@app.route("/expenses/grouped", methods=["GET"])
def get_grouped_expenses():
    expenses = crud.get_all_expenses()
    grouped = defaultdict(lambda: {"expenses": [], "total": 0})

    for e in expenses:
        date_obj = datetime.datetime.strptime(e['date'], "%Y-%m-%d")
        month = date_obj.strftime("%B %Y")  # e.g., "September 2025"
        grouped[month]["expenses"].append(e)
        grouped[month]["total"] += float(e['amount'])

    return jsonify(grouped)

if __name__ == "__main__":
    app.run(debug=True)
