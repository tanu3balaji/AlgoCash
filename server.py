import mysql.connector 
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import random

app = Flask(__name__)
CORS(app)
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Change if you have a different MySQL username
    password="Visha@99",  # Change this to your actual MySQL password
    database="keystroke_auth"
)
cursor = db.cursor()
# Sample user profile data (store in a database in real-world use)
user_profiles = {
    "user123": {
        "baseline_speed": 5.0,  # Average characters per second
        "security_questions": [
            {"question": "What is your pet’s name?", "answer": "Fluffy"},
            {"question": "What is your mother’s maiden name?", "answer": "Smith"},
            {"question": "Which city were you born in?", "answer": "Chennai"},
        ],
    }
}

@app.route("/keystroke-data", methods=["POST"])
def analyze_keystroke():
    data = request.json
    user_id = data.get("user_id")
    typing_speed = data.get("typing_speed")
    cursor.execute("SELECT baseline_speed FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    if user_id not in user_profiles:
        return jsonify({"status": "Error", "message": "User not found"}), 400

    baseline_speed = user_profiles[user_id]["baseline_speed"]
    deviation = abs(typing_speed - baseline_speed)

    if deviation > 1.5:  # Threshold for triggering security question
        security_question = random.choice(user_profiles[user_id]["security_questions"])
        return jsonify({"status": "Anomaly detected", "action": "Trigger Security Question", "question": security_question["question"]})

    return jsonify({"status": "Authenticated", "action": "Allow Access"})

@app.route("/verify-security-answer", methods=["POST"])
def verify_security_answer():
    data = request.json
    user_id = data.get("user_id")
    answer = data.get("answer").strip().lower()
    cursor.execute("SELECT answer FROM security_questions WHERE user_id = %s", (user_id,))
    stored_answer = cursor.fetchone()
    if stored_answer and stored_answer[0].strip().lower() == answer:
        return jsonify({"status": "Authenticated", "action": "Access Granted"})

    if user_id not in user_profiles:
        return jsonify({"status": "Error", "message": "User not found"}), 400

    for question in user_profiles[user_id]["security_questions"]:
        if answer == question["answer"].strip().lower():
            return jsonify({"status": "Authenticated", "action": "Access Granted"})

    return jsonify({"status": "Failed", "message": "Incorrect answer, access denied"}), 403
@app.route('/keystroke-data', methods=['POST'])
def keystroke_data():
    data = request.json
    print("Received keystroke data:", data)  # This prints the received data in the terminal
    return jsonify({"message": "Data received!"}), 200

@app.route('/')
def home():
    return "Flask server is running!"

if __name__ == '__main__':
    print("🚀 Flask server is starting on http://127.0.0.1:5000/")
    app.run(debug=True)