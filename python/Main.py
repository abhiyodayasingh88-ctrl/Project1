from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import psycopg2
import hashlib
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/")
def home():
    return send_file("index.html")

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not name or not username or not password:
        return jsonify({'success': False, 'message': 'Saare fields bharein!'}), 400

    hashed = hash_password(password)
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
            (name, username, hashed)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Account ban gaya!', 'name': name})
    except psycopg2.errors.UniqueViolation:
        return jsonify({'success': False, 'message': 'Username already exists!'}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username aur password daalein!'}), 400

    hashed = hash_password(password)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM users WHERE username=%s AND password=%s",
        (username, hashed)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'success': True, 'message': 'Login successful!', 'name': user[0]})
    else:
        return jsonify({'success': False, 'message': 'Galat username ya password!'}), 401

if __name__ == '__main__':
    print("Server running...")
    app.run(host='0.0.0.0', port=10000)