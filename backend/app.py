from flask import Flask, jsonify, request
import sqlite3
import subprocess
from flask_cors import CORS  # ✅ Import CORS
app = Flask(__name__)
CORS(app)  # ✅ Enable CORS globally
DB_NAME = "data/pokemon.db"

@app.route("/etl", methods=["POST"])
def trigger_etl():
    result = subprocess.run(["python", "pokemon_etl.py"], capture_output=True, text=True)
    return jsonify({
        "status": "ETL triggered",
        "output": result.stdout
    })

@app.route("/pokemon", methods=["GET"])
def get_pokemon():
    query = request.args.get("q", "")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if query:
        cursor.execute("SELECT id, name, height, weight FROM Pokemon WHERE name LIKE ?", (f"%{query}%",))
    else:
       cursor.execute("SELECT id, name, height, weight FROM Pokemon LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "height": r[2], "weight": r[3]} for r in rows])
@app.route('/')
def index():
    return "Welcome to the default index page!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
