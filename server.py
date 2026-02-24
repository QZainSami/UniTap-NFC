from flask import Flask, request, jsonify

app = Flask(__name__)

# --- SIMULATED DATABASE ---
# Replace '12345' with your actual RFID UID hex string
# --- SIMULATED DATABASE ---
users = {
    "F6B09103": {"name": "Samiullah", "balance": 1000.00},  # <--- YOUR CARD ID HERE
    "5C036B6E": {"name": "Sami_Test", "balance": 1000000.00}
}

PRICE_PER_TAP = 100.00

@app.route('/check-status', methods=['GET'])
def check_status():
    """Handshake endpoint to verify server is online"""
    print("--- Handshake received from UniTap Terminal ---")
    return jsonify({
        "status": "ONLINE",
        "price": PRICE_PER_TAP  # <--- Now sending the price!
    }), 200

@app.route('/payment', methods=['POST'])
def process_payment():
    """Main payment processing endpoint"""
    data = request.get_json()
    uid = data.get("uid", "").strip()
    
    print(f"Incoming Tap: UID [{uid}]")

    # 1. Check if user exists
    if uid not in users:
        print("Result: DECLINED - Unknown Card")
        return jsonify({
            "status": "DECLINED",
            "name": "UNKNOWN",
            "msg": "Invalid Card"
        }), 200

    user = users[uid]

    # 2. Check Balance
    if user["balance"] >= PRICE_PER_TAP:
        user["balance"] -= PRICE_PER_TAP
        print(f"Result: SUCCESS - {user['name']} paid Rs. {PRICE_PER_TAP}")
        return jsonify({
            "status": "SUCCESS",
            "name": user['name'],
            "msg": f"Bal: Rs.{user['balance']:.0f}"
        }), 200
    else:
        print(f"Result: DECLINED - {user['name']} has Insufficient Funds")
        return jsonify({
            "status": "DECLINED",
            "name": user['name'],
            "msg": "Low Balance"
        }), 200

if __name__ == '__main__':
    # ssl_context='adhoc' automatically generates a temporary security certificate
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')