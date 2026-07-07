from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Database connection configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Change to your MySQL password
    "database": "staticprofiledb",        # Change to your database name
    "port": 3306
}

def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

# Get all contacts
@app.route("/contact", methods=["GET"])
def get_contacts():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, email, message FROM Contact")
        rows = cursor.fetchall()
        return jsonify(rows)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Add a new contact
@app.route("/contact", methods=["POST"])
def add_contact():
    data = request.get_json()

    # Basic input validation
    if not data or not all(k in data for k in ("name", "email", "message")):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        sql = "INSERT INTO Contact (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data["name"], data["email"], data["message"]))
        conn.commit()
        return jsonify({"message": "Contact added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
