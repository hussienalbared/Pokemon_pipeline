import os
from time import sleep

from config import DB_NAME, POKEMON_IDS
from api import fetch_pokemon_data
from db import PokemonDB

def main():
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)

    db = PokemonDB(DB_NAME)

    for pid in POKEMON_IDS:
        try:
            print(f"Processing Pokémon ID {pid}")
            data = fetch_pokemon_data(pid)
            db.insert_pokemon(data)
            sleep(0.5)  # Respect API rate limits
        except Exception as e:
            print(f"Error processing Pokémon ID {pid}: {e}")

    db.close()

if __name__ == "__main__":
    main()
