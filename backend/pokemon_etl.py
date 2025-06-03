import requests
import sqlite3
import json
from time import sleep
import os
# --- Constants ---
DB_NAME = 'data/pokemon.db'

POKEMON_IDS = range(1, 11)  # First 20 Pokémon

# --- Database Setup ---
def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT,
        base_experience INTEGER,
        height INTEGER,
        weight INTEGER
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Type (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PokemonType (
        pokemon_id INTEGER,
        type_id INTEGER,
        FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
        FOREIGN KEY (type_id) REFERENCES Type(id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PokemonAbility (
        pokemon_id INTEGER,
        ability_id INTEGER,
        is_hidden BOOLEAN,
        FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
        FOREIGN KEY (ability_id) REFERENCES Ability(id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PokemonStat (
        pokemon_id INTEGER,
        stat_id INTEGER,
        base_stat INTEGER,
        effort INTEGER,
        FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
        FOREIGN KEY (stat_id) REFERENCES Stat(id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EvolutionChain (
        id INTEGER PRIMARY KEY,
        chain TEXT
    )''')

    conn.commit()

# --- Helper Functions ---
def get_or_create_id(cursor, table, name):
    cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
    return cursor.lastrowid

def extract_pokemon_data(pokemon_id):
    base_url = "https://pokeapi.co/api/v2"
    pokemon = requests.get(f"{base_url}/pokemon/{pokemon_id}").json()
    species = requests.get(pokemon["species"]["url"]).json()
    evo_chain_url = species["evolution_chain"]["url"]
    evo_chain = requests.get(evo_chain_url).json()

    return {
        "id": pokemon["id"],
        "name": pokemon["name"],
        "base_experience": pokemon["base_experience"],
        "height": pokemon["height"],
        "weight": pokemon["weight"],
        "types": [t["type"]["name"] for t in pokemon["types"]],
        "abilities": [
            {"name": a["ability"]["name"], "is_hidden": a["is_hidden"]}
            for a in pokemon["abilities"]
        ],
        "stats": [
            {"name": s["stat"]["name"], "base_stat": s["base_stat"], "effort": s["effort"]}
            for s in pokemon["stats"]
        ],
        "evolution_chain_id": evo_chain["id"],
        "evolution_chain": evo_chain["chain"],
    }

def insert_pokemon_data(conn, data):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO Pokemon (id, name, base_experience, height, weight)
        VALUES (?, ?, ?, ?, ?)""",
        (data["id"], data["name"], data["base_experience"], data["height"], data["weight"])
    )

    # Types
    for type_name in data["types"]:
        type_id = get_or_create_id(cursor, "Type", type_name)
        cursor.execute("INSERT INTO PokemonType (pokemon_id, type_id) VALUES (?, ?)", (data["id"], type_id))

    # Abilities
    for ability in data["abilities"]:
        ability_id = get_or_create_id(cursor, "Ability", ability["name"])
        cursor.execute("""
            INSERT INTO PokemonAbility (pokemon_id, ability_id, is_hidden)
            VALUES (?, ?, ?)""",
            (data["id"], ability_id, ability["is_hidden"])
        )

    # Stats
    for stat in data["stats"]:
        stat_id = get_or_create_id(cursor, "Stat", stat["name"])
        cursor.execute("""
            INSERT INTO PokemonStat (pokemon_id, stat_id, base_stat, effort)
            VALUES (?, ?, ?, ?)""",
            (data["id"], stat_id, stat["base_stat"], stat["effort"])
        )

    # Evolution Chain
    cursor.execute("""
        INSERT OR IGNORE INTO EvolutionChain (id, chain)
        VALUES (?, ?)""",
        (data["evolution_chain_id"], json.dumps(data["evolution_chain"]))
    )

    conn.commit()

# --- Main ETL ---
def main():
    
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)  # Ensure folder exists
    conn = sqlite3.connect(DB_NAME)
    create_tables(conn)

    for pokemon_id in POKEMON_IDS:
        try:
            print(f"Processing Pokémon ID {pokemon_id}")
            data = extract_pokemon_data(pokemon_id)
            insert_pokemon_data(conn, data)
            sleep(0.5)  # Be nice to the API
        except Exception as e:
            print(f"Error on Pokémon ID {pokemon_id}: {e}")

    conn.close()

if __name__ == "__main__":
    main()
