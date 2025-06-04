from flask import Blueprint, request, jsonify
from db.base import get_db

filter_bp = Blueprint('filter_bp', __name__)

@filter_bp.route('/api/pokemons')
def filter_pokemons():
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
    if 'min_exp' in args:
        filters.append("p.base_experience >= ?")
        params.append(args['min_exp'])
    if 'max_exp' in args:
        filters.append("p.base_experience <= ?")
        params.append(args['max_exp'])

    if filters:
        base_query += " AND " + " AND ".join(filters)

    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])
