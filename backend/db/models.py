# db/models.py

from db.schema import create_tables
from db.base import get_or_create_id
import json
import sqlite3
from typing import Dict

class PokemonDB:
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
