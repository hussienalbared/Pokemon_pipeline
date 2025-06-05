import sqlite3
from config import DB_NAME
from graphql2.types import Pokemon, Type, Ability, Stat

def get_pokemon_by_id(pokemon_id: int) -> Pokemon | None:
    """
    Retrieve a Pokémon and its related data from the database by its ID.
    Args:
        pokemon_id (int): The unique identifier of the Pokémon to retrieve.
    Returns:
        Pokemon | None: A `Pokemon` object populated with its base attributes, types, abilities, and stats
        if found; otherwise, `None` if no Pokémon with the given ID exists.
    Database Tables Accessed:
        - Pokemon: Base Pokémon data.
        - Type, PokemonType: Pokémon's types.
        - Ability, PokemonAbility: Pokémon's abilities and whether they are hidden.
        - Stat, PokemonStat: Pokémon's stats and effort values.
    Raises:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Base Pokémon
    cur.execute("SELECT * FROM Pokemon WHERE id = ?", (pokemon_id,))
    row = cur.fetchone()
    if not row:
        return None

    # Types
    cur.execute("""
        SELECT t.id, t.name FROM Type t
        JOIN PokemonType pt ON t.id = pt.type_id
        WHERE pt.pokemon_id = ?
    """, (pokemon_id,))
    types = [Type(**dict(r)) for r in cur.fetchall()]

    # Abilities
    cur.execute("""
        SELECT a.id, a.name, pa.is_hidden FROM Ability a
        JOIN PokemonAbility pa ON a.id = pa.ability_id
        WHERE pa.pokemon_id = ?
    """, (pokemon_id,))
    abilities = [Ability(id=r["id"], name=r["name"], is_hidden=bool(r["is_hidden"])) for r in cur.fetchall()]

    # Stats
    cur.execute("""
        SELECT s.name, ps.base_stat, ps.effort FROM Stat s
        JOIN PokemonStat ps ON s.id = ps.stat_id
        WHERE ps.pokemon_id = ?
    """, (pokemon_id,))
    stats = [Stat(name=r["name"], base_stat=r["base_stat"], effort=r["effort"]) for r in cur.fetchall()]

    conn.close()

    return Pokemon(
        id=row["id"],
        name=row["name"],
        base_experience=row["base_experience"],
        height=row["height"],
        weight=row["weight"],
        types=types,
        abilities=abilities,
        stats=stats
    )
