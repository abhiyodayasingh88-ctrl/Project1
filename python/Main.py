from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import os

app = Flask(__name__)
CORS(app)  # Frontend se connect hone deta hai

DB_NAME = "users.db"

# ─── Database Setup ───────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ─── SIGNUP API ───────────────────────────────────────────────
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name     = data.get('name', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not name or not username or not password:
        return jsonify({'success': False, 'message': 'Saare fields bharein!'}), 400

    hashed = hash_password(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
            (name, username, hashed)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Account ban gaya!', 'name': name})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Username already exists!'}), 409

# ─── LOGIN API ────────────────────────────────────────────────
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username aur password daalein!'}), 400

    hashed = hash_password(password)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM users WHERE username=? AND password=?",
        (username, hashed)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'success': True, 'message': 'Login successful!', 'name': user[0]})
    else:
        return jsonify({'success': False, 'message': 'Galat username ya password!'}), 401

# ─── Run Server ───────────────────────────────────────────────
@app.route("/")
def home():
    return "Server Running Successfully!"

if __name__ == '__main__':
    init_db()
    print("✅ Server running: http://localhost:5000")
    app.run(debug=True, port=5000)