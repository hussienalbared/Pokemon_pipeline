# db/schema.py

def create_tables(conn):
    """
    Creates all necessary tables for the Pokémon database schema if they do not already exist.
    Tables created:
    - Pokemon: Stores basic information about each Pokémon.
    - Type: Stores unique Pokémon types.
    - PokemonType: Associates Pokémon with their types (many-to-many relationship).
    - Ability: Stores unique abilities.
    - PokemonAbility: Associates Pokémon with their abilities, including whether the ability is hidden.
    - Stat: Stores unique stats.
    - PokemonStat: Associates Pokémon with their stats, including base stat and effort values.
    - EvolutionChain: Stores evolution chain information for Pokémon.
    Args:
        conn (sqlite3.Connection): The SQLite database connection object.
    Commits the changes to the database after creating the tables.
    """
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT,
        base_experience INTEGER,
        height INTEGER,
        weight INTEGER
    );

    CREATE TABLE IF NOT EXISTS Type (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS PokemonType (
        pokemon_id INTEGER,
        type_id INTEGER,
        FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
        FOREIGN KEY (type_id) REFERENCES Type(id)
    );

    CREATE TABLE IF NOT EXISTS Ability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS PokemonAbility (
        pokemon_id INTEGER,
        ability_id INTEGER,
        is_hidden BOOLEAN,
        FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
        FOREIGN KEY (ability_id) REFERENCES Ability(id)
    );

    CREATE TABLE IF NOT EXISTS Stat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS PokemonStat (
        pokemon_id INTEGER,
        stat_id INTEGER,
        base_stat INTEGER,
        effort INTEGER,
        FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
        FOREIGN KEY (stat_id) REFERENCES Stat(id)
    );

    CREATE TABLE IF NOT EXISTS EvolutionChain (
        id INTEGER PRIMARY KEY,
        chain TEXT
    );
    """)
    conn.commit()
