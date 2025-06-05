# etl_routes.py
from flask import Blueprint, jsonify, request
from pipeline.etl_job import run_etl  # ✅ import the function

etl_bp = Blueprint('etl_bp', __name__)

@etl_bp.route("/etl", methods=["POST"])
def trigger_etl():
    """
    Endpoint to trigger the ETL (Extract, Transform, Load) process for specified Pokémon IDs.
    Expects a JSON payload with a list of Pokémon IDs under the "ids" key.
    Returns a JSON response indicating the status of the ETL trigger or an error message.
    Request:
        POST /etl
        Content-Type: application/json
        Body: { "ids": [<int>, ...] }
    Responses:
        200: { "status": "ETL triggered" }
        400: { "error": "No Pokémon IDs provided" }
        500: { "error": "<error message>" }
    """
    data = request.get_json()
    pokemon_ids = data.get("ids", [])

    if not pokemon_ids:
        return jsonify({"error": "No Pokémon IDs provided"}), 400

    try:
            
            result = run_etl(pokemon_ids)  # ✅ direct function call
            return jsonify({
                "status": "ETL triggered"
            })
    except Exception as e:
            return jsonify({"error": str(e)}), 500