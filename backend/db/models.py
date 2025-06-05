# db/models.py

from db.schema import create_tables
from db.base import get_or_create_id
import json
import sqlite3
from typing import Dict

class PokemonDB:
    """
    A database handler class for managing Pokémon data using SQLite.
    Args:
        db_path (str): Path to the SQLite database file.
    Methods:
        insert_pokemon(data: Dict):
            Inserts or updates a Pokémon and its related data (types, abilities, stats, evolution chain) into the database.
            Args:
                data (Dict): A dictionary containing Pokémon data with keys:
                    - id (int): Pokémon ID.
                    - name (str): Pokémon name.
                    - base_experience (int): Base experience value.
                    - height (int): Height of the Pokémon.
                    - weight (int): Weight of the Pokémon.
                    - types (List[str]): List of type names.
                    - abilities (List[Dict]): List of abilities, each with 'name' (str) and 'is_hidden' (bool).
                    - stats (List[Dict]): List of stats, each with 'name' (str), 'base_stat' (int), and 'effort' (int).
                    - evolution_chain_id (int): ID of the evolution chain.
                    - evolution_chain (Any): Evolution chain data (serializable to JSON).
        close():
            Closes the database connection.
    """
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        create_tables(self.conn)

    def insert_pokemon(self, data: Dict):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO Pokemon (id, name, base_experience, height, weight)
            VALUES (?, ?, ?, ?, ?)""",
            (data["id"], data["name"], data["base_experience"], data["height"], data["weight"])
        )

        for type_name in data["types"]:
            type_id = get_or_create_id(self.conn, "Type", type_name)
            cursor.execute("INSERT INTO PokemonType (pokemon_id, type_id) VALUES (?, ?)", (data["id"], type_id))

        for ability in data["abilities"]:
            ability_id = get_or_create_id(self.conn, "Ability", ability["name"])
            cursor.execute("""
                INSERT INTO PokemonAbility (pokemon_id, ability_id, is_hidden)
                VALUES (?, ?, ?)""",
                (data["id"], ability_id, ability["is_hidden"])
            )

        for stat in data["stats"]:
            stat_id = get_or_create_id(self.conn, "Stat", stat["name"])
            cursor.execute("""
                INSERT INTO PokemonStat (pokemon_id, stat_id, base_stat, effort)
                VALUES (?, ?, ?, ?)""",
                (data["id"], stat_id, stat["base_stat"], stat["effort"])
            )

        cursor.execute("""
            INSERT OR IGNORE INTO EvolutionChain (id, chain)
            VALUES (?, ?)""",
            (data["evolution_chain_id"], json.dumps(data["evolution_chain"]))
        )

        self.conn.commit()

    def close(self):
        self.conn.close()
