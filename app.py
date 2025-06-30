import sqlite3
import random
from flask import Flask, session, render_template, request, g

app = Flask(__name__)
app.secret_key = "select_a_COMPLEX_secret_key_please"  # Use a secure key for production

# Home route
@app.route('/')
def index():
    all_items, shopping_list = get_items_from_db()
    session['all_items'] = all_items
    session['shopping_items'] = shopping_list
    return render_template("index.html", all_items=all_items, shopping_items=shopping_list)

# Add item to shopping list
@app.route('/add_item', methods=["POST"])
def add_item():
    selected_item = request.form.get("select_items")
    if not selected_item:
        return render_template("index.html", all_items=session.get('all_items', []), shopping_items=session.get('shopping_items', []))

    if "shopping_items" not in session:
        session["shopping_items"] = []

    if selected_item not in session["shopping_items"]:
        session["shopping_items"].append(selected_item)
        session.modified = True

    return render_template("index.html", all_items=session['all_items'], shopping_items=session['shopping_items'])

# Remove selected items
@app.route('/remove_items', methods=["POST"])
def remove_items():
    if "shopping_items" not in session:
        session["shopping_items"] = []

    checked_boxes = request.form.getlist("remove_items")

    for item in checked_boxes:
        if item in session["shopping_items"]:
            session["shopping_items"].remove(item)
            session.modified = True

    return render_template("index.html", all_items=session['all_items'], shopping_items=session['shopping_items'])

# Get data from SQLite DB
def get_items_from_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('grocery_list.db')
    cursor = db.cursor()
    cursor.execute("SELECT name FROM groceries")
    all_items = [row[0] for row in cursor.fetchall()]
    random.shuffle(all_items)
    shopping_list = all_items[:5] if len(all_items) >= 5 else all_items
    return all_items, shopping_list

# Close DB connection
@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('_database', None)
    if db is not None:
        db.close()

# Run app
if __name__ == '__main__':
    app.run(debug=True)
