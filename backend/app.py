from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
import time

app = Flask(__name__)
CORS(app)

while True:
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            database=os.environ.get("DB_NAME", "appdb"),
            user=os.environ.get("DB_USER", "appuser"),
            password=os.environ.get("DB_PASSWORD", "password")
        )
        break
    except Exception as e:
        print("Waiting for database...")
        time.sleep(2)

@app.route("/messages", methods=["GET", "POST"])
def messages():
    cur = conn.cursor()

    if request.method == "POST":
        text = request.json.get("text")
        cur.execute("INSERT INTO messages (text) VALUES (%s)", (text,))
        conn.commit()
        return jsonify({"status": "ok"})

    cur.execute("SELECT text FROM messages")
    rows = cur.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
