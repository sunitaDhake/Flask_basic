from flask import Flask, render_template, request, g  # Import necessary modules from Flask package
import sqlite3  # Import SQLite module to connect with database store the data 
import threading  # Import threading module for executing database operations in separate threads

app = Flask(__name__)  # Create a Flask application instance


def get_db():
    """Helper function to create a SQLite connection."""
    if 'db' not in g:  # Check if the database connection is already stored in the Flask application context
        g.db = sqlite3.connect('database.db')  # Create a SQLite connection and store it in the Flask application context
    return g.db  # Return the SQLite connection


@app.teardown_appcontext
def close_db(error):
    """Close the SQLite connection at the end of the request."""
    db = g.pop('db', None)  # Retrieve the SQLite connection from the Flask application context
    if db is not None:  # Check if the connection exists
        db.close()  # Close the SQLite connection


@app.route("/")
def home():
    return render_template("registration.html")  # Render the "registration.html" template and return it


@app.route("/register", methods=["POST"])
def register():
    try:
        name = request.form.get("name")  # Get the value of the "name" field from the form data
        email = request.form.get("email")  # Get the value of the "email" field from the form data
        password = request.form.get("password")  # Get the value of the "password" field from the form data

        conn = get_db()  # Get the SQLite connection
        cursor = conn.cursor()  # Create a cursor object to execute SQL statements

        # Insert the form data into the "registrations" table
        cursor.execute("INSERT INTO registrations (name, email, password) VALUES (?, ?, ?)",
                       (name, email, password))
        conn.commit()  # Commit the changes to the database

        return f"Thank you for registering, {name}!"  # Return a success message
    except Exception as e:
        return f"An error occurred: {e}"  # Return an error message if an exception occurs


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)  # Start the Flask development server on localhost:5000
