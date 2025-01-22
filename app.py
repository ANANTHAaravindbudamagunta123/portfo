from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Function to initialize the database and create the contacts table
def initialize_database():
    try:
        with sqlite3.connect('contact_form.db') as conn:
            cursor = conn.cursor()
            # Create table if it doesn't exist
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            )
            """)
            print("Database initialized and table created successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Function to insert contact form data into the database
def insert_contact(name, email, message):
    try:
        with sqlite3.connect('contact_form.db') as conn:
            cursor = conn.cursor()
            # Insert data into the contacts table
            cursor.execute("""
            INSERT INTO contacts (name, email, message, timestamp)
            VALUES (?, ?, ?, ?)
            """, (name, email, message, datetime.now()))
            print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Contact form submission route
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Simple server-side validation
        if not name or not email or not message:
            flash("All fields are required!", "error")
            return redirect(url_for('index'))

        # Insert the form data into the database
        insert_contact(name, email, message)
        flash("Data submitted successfully!", "success")  # Success message
        return redirect(url_for('index'))  # Redirect back to the home page after submission

if __name__ == '__main__':
    initialize_database()  # Ensure the database and table are set up
    app.run(debug=True)
