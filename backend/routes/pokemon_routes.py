from flask import Blueprint, jsonify, abort
from db.base import get_db

pokemon_bp = Blueprint('pokemon_bp', __name__)

@pokemon_bp.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
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
    from flask import request
    query = request.args.get("q", "")
    db = get_db()
    cursor = db.cursor()
    if query:
        cursor.execute("SELECT id, name, height, weight FROM Pokemon WHERE name LIKE ?", (f"%{query}%",))
    else:
        cursor.execute("SELECT id, name, height, weight FROM Pokemon LIMIT 50")
    rows = cursor.fetchall()
    return jsonify([{"id": r[0], "name": r[1], "height": r[2], "weight": r[3]} for r in rows])
