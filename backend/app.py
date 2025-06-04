from flask import Flask, jsonify, request
from flask import abort, g
import sqlite3
import subprocess
from flask_cors import CORS  # ✅ Import CORS
# from flask_graphql import GraphQLView
# from graphql_schema import schema
app = Flask(__name__)
CORS(app)  # ✅ Enable CORS globally
DB_NAME = "data/pokemon.db"
# app.add_url_rule(
#     "/graphql",
#     view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
# )

@app.route("/etl", methods=["POST"])
def trigger_etl():
    result = subprocess.run(["python", "pokemon_etl.py"], capture_output=True, text=True)
    return jsonify({
        "status": "ETL triggered",
        "output": result.stdout
    })

@app.route("/pokemon", methods=["GET"])
def get_pokemons():
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


@app.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
    db = get_db()

    # Fetch basic pokemon info
    pokemon = db.execute(
        "SELECT * FROM Pokemon WHERE LOWER(name) = LOWER(?)", (name,)
    ).fetchone()

    if not pokemon:
        abort(404, description="Pokémon not found")

    pokemon_id = pokemon['id']

    # Fetch types
    types = db.execute('''
        SELECT Type.name FROM Type
        JOIN PokemonType ON Type.id = PokemonType.type_id
        WHERE PokemonType.pokemon_id = ?
    ''', (pokemon_id,)).fetchall()

    # Fetch abilities (with is_hidden flag)
    abilities = db.execute('''
        SELECT Ability.name, PokemonAbility.is_hidden FROM Ability
        JOIN PokemonAbility ON Ability.id = PokemonAbility.ability_id
        WHERE PokemonAbility.pokemon_id = ?
    ''', (pokemon_id,)).fetchall()

    # Fetch stats
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


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_NAME)
        db.row_factory = sqlite3.Row
    return db
@app.route('/api/pokemons')
def filter_pokemons():
    args = request.args
    conn =  get_db()
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

    # Filter by name (substring, case-insensitive)
    if 'name' in args:
        filters.append("LOWER(p.name) LIKE ?")
        params.append(f"%{args['name'].lower()}%")

    # Filter by type (exact match)
    if 'type' in args:
        filters.append("LOWER(t.name) = ?")
        params.append(args['type'].lower())

    # Filter by ability (exact match)
    if 'ability' in args:
        filters.append("LOWER(a.name) = ?")
        params.append(args['ability'].lower())

    # Filter by base_experience
    if 'min_exp' in args:
        filters.append("p.base_experience >= ?")
        params.append(args['min_exp'])

    if 'max_exp' in args:
        filters.append("p.base_experience <= ?")
        params.append(args['max_exp'])

    # Append filters to the query
    if filters:
        base_query += " AND " + " AND ".join(filters)

    cursor.execute(base_query, params)
    rows = cursor.fetchall()

    # Convert to list of dicts
    pokemons = [dict(row) for row in rows]
    return jsonify(pokemons)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
