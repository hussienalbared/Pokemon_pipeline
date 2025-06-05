from flask import Blueprint, request, jsonify
from db.base import get_db

filter_bp = Blueprint('filter_bp', __name__)

@filter_bp.route('/api/pokemons')
def filter_pokemons():
    """
    Endpoint to filter and retrieve Pokémon based on query parameters.
    This route handles GET requests to '/api/pokemons' and allows filtering Pokémon
    by id, name, type, and ability. The filters are applied dynamically based on the
    provided query parameters.

    Query Parameters:
        id (int, optional): The unique identifier of the Pokémon.
        name (str, optional): A substring to search for in the Pokémon's name (case-insensitive).
        type (str, optional): The name of the Pokémon's type (case-insensitive).
        ability (str, optional): The name of the Pokémon's ability (case-insensitive).

    Returns:
        flask.Response: A JSON array of Pokémon objects matching the filters, where each object contains:
            - id (int): Pokémon's unique identifier.
            - name (str): Pokémon's name.
            - base_experience (int): Pokémon's base experience value.
            - height (int): Pokémon's height.
            - weight (int): Pokémon's weight.
    """
    args = request.args
    conn = get_db()
    cursor = conn.cursor()

    base_query = """
        SELECT DISTINCT p.id, p.name, p.base_experience, p.height, p.weight
        FROM Pokemon p
        LEFT JOIN PokemonType pt ON p.id = pt.pokemon_id
        LEFT JOIN Type t ON pt.type_id = t.id
        LEFT JOIN PokemonAbility pa ON p.id = pa.pokemon_id
        LEFT JOIN Ability a ON pa.ability_id = a.id
        WHERE 1=1
    """
    filters = []
    params = []
    if 'id' in args:
        filters.append("p.id = ?")
        params.append(args['id'])

    if 'name' in args:
        filters.append("LOWER(p.name) LIKE ?")
        params.append(f"%{args['name'].lower()}%")
    if 'type' in args:
        filters.append("LOWER(t.name) = ?")
        params.append(args['type'].lower())
    if 'ability' in args:
        filters.append("LOWER(a.name) = ?")
        params.append(args['ability'].lower())

    if filters:
        base_query += " AND " + " AND ".join(filters)

    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])
