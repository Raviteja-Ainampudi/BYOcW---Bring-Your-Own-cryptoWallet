from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit
import os
import json
import sqlite3
from utils import save_qr_code, save_wallet

app = Flask(__name__)
socketio = SocketIO(app)

# Ensure the "templates" folder is in the correct directory
app.template_folder = os.path.join(os.path.dirname(__file__), "templates")

# File-based JSON storage
JSON_FILE = "wallets.json"
DATABASE_FILE = "wallets.db"

# Initialize JSON file
def init_json_file():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as f:
            json.dump([], f)

# Initialize SQLite database
def init_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency TEXT NOT NULL,
                address TEXT NOT NULL,
                encrypted_private_key TEXT NOT NULL,
                qr_code TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                recipient TEXT NOT NULL,
                currency TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)
        conn.commit()

# Add wallet to JSON file
def add_wallet_to_json(wallet):
    with open(JSON_FILE, "r+") as f:
        data = json.load(f)
        data.append(wallet)
        f.seek(0)
        json.dump(data, f)

# Add wallet to SQLite
def add_wallet_to_db(currency, address, encrypted_private_key, qr_code):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO wallets (currency, address, encrypted_private_key, qr_code)
            VALUES (?, ?, ?, ?)
        """, (currency, address, encrypted_private_key, qr_code))
        conn.commit()

# Retrieve wallets from SQLite
def get_all_wallets():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT currency, address, encrypted_private_key, qr_code FROM wallets")
        return [{"currency": row[0], "address": row[1], "encrypted_private_key": row[2], "qr_code": row[3]} for row in cursor.fetchall()]

@app.route('/')
def dashboard():
    """
    Serve the dashboard HTML.
    """
    return render_template("dashboard.html")

@app.route('/create_wallet/<currency>', methods=['GET'])
def create_wallet(currency):
    """
    Create a wallet for the specified cryptocurrency.
    """
    if currency.lower() not in ["ethereum", "bitcoin"]:
        return jsonify({"error": "Unsupported currency"}), 400
    address = f"{currency}_address_{os.urandom(4).hex()}"
    private_key = f"{currency}_private_key_{os.urandom(4).hex()}"
    encrypted_key_path = save_wallet(address, private_key)
    qr_code_path = save_qr_code(address)

    # Save wallet to both JSON and SQLite
    wallet_info = {
        "currency": currency.capitalize(),
        "address": address,
        "encrypted_private_key": encrypted_key_path,
        "qr_code": qr_code_path,
    }
    add_wallet_to_json(wallet_info)
    add_wallet_to_db(currency.capitalize(), address, encrypted_key_path, qr_code_path)

    # Emit real-time update to the UI
    socketio.emit('wallet_update', wallet_info)
    return jsonify(wallet_info)

@app.route('/api/wallets', methods=['GET'])
def get_wallets():
    """
    Return all wallets as JSON.
    """
    return jsonify(get_all_wallets())

@app.route('/send_currency', methods=['POST'])
def send_currency():
    """
    Simulate sending currency from one wallet to another.
    """
    data = request.json
    sender = data.get("sender")
    recipient = data.get("recipient")
    currency = data.get("currency")
    amount = data.get("amount")

    if not all([sender, recipient, currency, amount]):
        return jsonify({"error": "Invalid input"}), 400

    # Check if sender wallet exists
    wallets = get_all_wallets()
    sender_wallet = next((w for w in wallets if w["address"] == sender and w["currency"].lower() == currency.lower()), None)
    if not sender_wallet:
        return jsonify({"error": "Sender wallet not found"}), 404

    # Simulate transaction success
    transaction_status = "success"

    # Log the transaction
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (sender, recipient, currency, amount, status)
            VALUES (?, ?, ?, ?, ?)
        """, (sender, recipient, currency.capitalize(), amount, transaction_status))
        conn.commit()

    return jsonify({"message": f"{amount} {currency} sent from {sender} to {recipient}!", "status": transaction_status})

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """
    Retrieve all transactions.
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sender, recipient, currency, amount, status FROM transactions")
        return jsonify([{
            "sender": row[0],
            "recipient": row[1],
            "currency": row[2],
            "amount": row[3],
            "status": row[4]
        } for row in cursor.fetchall()])

@app.route('/api/health', methods=['GET'])
def api_health():
    """
    Check API health status.
    """
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    init_json_file()
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
