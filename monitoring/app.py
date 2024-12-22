from flask import Flask, request, jsonify, session, render_template, send_from_directory
import json
import os
from concurrent.futures import ThreadPoolExecutor
import requests
import ssl
import socket

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Paths for data storage
USER_FILE = 'users.json'
DOMAIN_FOLDER = 'domains'

if not os.path.exists(DOMAIN_FOLDER):
    os.makedirs(DOMAIN_FOLDER)

def validate_registration(username, password):
    with open(USER_FILE, 'r') as f:
        users = json.load(f)
    if username in users:
        return False, 'Username already exists'
    users[username] = password
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)
    return True, 'Registration successful'

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    status, msg = validate_registration(username, password)
    if status:
        return jsonify({'status': 'success', 'message': msg})
    else:
        return jsonify({'status': 'failed', 'message': msg})

@app.route('/<filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('./static', filename)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
