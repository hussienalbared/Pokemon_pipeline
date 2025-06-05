from sqlite3 import Error
from flask import Blueprint, jsonify, abort, request
from db.base import get_db

pokemon_bp = Blueprint('pokemon_bp', __name__)

@pokemon_bp.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
    """
    Retrieve detailed information about a Pokémon by its name.
    This endpoint handles GET requests to '/pokemon/<name>' and returns a JSON object containing
    the Pokémon's basic information, types, abilities, and stats. If the Pokémon is not found,
    a 404 error is returned.
    Args:
        name (str): The name of the Pokémon to retrieve (case-insensitive).
    Returns:
        Response: A JSON response with the following structure:
            {
                'id': int,
                'name': str,
                'base_experience': int,
                'height': int,
                'weight': int,
                'types': List[str],
                'abilities': List[{'name': str, 'is_hidden': bool}],
                'stats': List[{'name': str, 'base_stat': int, 'effort': int}]
            }
    Raises:
        404: If the Pokémon with the specified name is not found in the database.
    """
    db = get_db()
    pokemon = db.execute(
        "SELECT * FROM Pokemon WHERE LOWER(name) = LOWER(?)", (name,)
    ).fetchone()

    if not pokemon:
        abort(404, description="Pokémon not found")

    pokemon_id = pokemon['id']

    types = db.execute('''
        SELECT Type.name FROM Type
        JOIN PokemonType ON Type.id = PokemonType.type_id
        WHERE PokemonType.pokemon_id = ?
    ''', (pokemon_id,)).fetchall()

    abilities = db.execute('''
        SELECT Ability.name, PokemonAbility.is_hidden FROM Ability
        JOIN PokemonAbility ON Ability.id = PokemonAbility.ability_id
        WHERE PokemonAbility.pokemon_id = ?
    ''', (pokemon_id,)).fetchall()

    stats = db.execute('''
        SELECT Stat.name, PokemonStat.base_stat, PokemonStat.effort FROM Stat
        JOIN PokemonStat ON Stat.id = PokemonStat.stat_id
        WHERE PokemonStat.pokemon_id = ?
    ''', (pokemon_id,)).fetchall()

    result = {
        'id': pokemon['id'],
        'name': pokemon['name'],
        'base_experience': pokemon['base_experience'],
        'height': pokemon['height'],
        'weight': pokemon['weight'],
        'types': [t['name'] for t in types],
        'abilities': [{'name': a['name'], 'is_hidden': bool(a['is_hidden'])} for a in abilities],
        'stats': [{'name': s['name'], 'base_stat': s['base_stat'], 'effort': s['effort']} for s in stats],
    }

    return jsonify(result)

@pokemon_bp.route("/pokemon", methods=["GET"])
def get_pokemons():
    limit = request.args.get("limit", default=50, type=int)
    offset = request.args.get("offset", default=0, type=int)

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT id, name, height, weight
            FROM Pokemon
            LIMIT ? OFFSET ?
            """, (limit, offset)
        )
        rows = cursor.fetchall()
        pokemons = [
            {"id": row[0], "name": row[1], "height": row[2], "weight": row[3]}
            for row in rows
        ]
        return jsonify(pokemons), 200
    except Error as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
