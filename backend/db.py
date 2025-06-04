import sqlite3
import json
from typing import List, Dict

class PokemonDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

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

        self.conn.commit()

    def get_or_create_id(self, table: str, name: str):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
        self.conn.commit()
        return cursor.lastrowid

    def insert_pokemon(self, data: Dict):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO Pokemon (id, name, base_experience, height, weight)
            VALUES (?, ?, ?, ?, ?)""",
            (data["id"], data["name"], data["base_experience"], data["height"], data["weight"])
        )

        # Types
        for type_name in data["types"]:
            type_id = self.get_or_create_id("Type", type_name)
            cursor.execute("INSERT INTO PokemonType (pokemon_id, type_id) VALUES (?, ?)", (data["id"], type_id))

        # Abilities
        for ability in data["abilities"]:
            ability_id = self.get_or_create_id("Ability", ability["name"])
            cursor.execute("""
                INSERT INTO PokemonAbility (pokemon_id, ability_id, is_hidden)
                VALUES (?, ?, ?)""",
                (data["id"], ability_id, ability["is_hidden"])
            )

        # Stats
        for stat in data["stats"]:
            stat_id = self.get_or_create_id("Stat", stat["name"])
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

        self.conn.commit()

    def close(self):
        self.conn.close()





