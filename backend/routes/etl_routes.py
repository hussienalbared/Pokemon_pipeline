# etl_routes.py
from flask import Blueprint, jsonify, request
import subprocess
import json
from pipeline.etl_job import run_etl  # ✅ import the function

etl_bp = Blueprint('etl_bp', __name__)

@etl_bp.route("/etl", methods=["POST"])
def trigger_etl():
    data = request.get_json()
    pokemon_ids = data.get("ids", [])

    if not pokemon_ids:
        return jsonify({"error": "No Pokémon IDs provided"}), 400

    try:
            
            result = run_etl(pokemon_ids)  # ✅ direct function call
            return jsonify({
                "status": "ETL triggered",
                "result": result
            })
    except Exception as e:
            return jsonify({"error": str(e)}), 500