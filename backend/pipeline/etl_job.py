import json
import os
import sys
import logging
from time import sleep

from pipeline.fetch_pokemon_data import fetch_pokemon_data
from config import DB_NAME
from db.models import PokemonDB

# 🔧 Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "etl.log"),
    level=logging.INFO
)

def run_etl(pokemon_ids):
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    db = PokemonDB(DB_NAME)

    logging.info("ETL process started")
    logging.info(f"Processing Pokémon IDs: {pokemon_ids}")
    
    for pid in pokemon_ids:
        try:
            logging.info(f"Processing Pokémon ID {pid}")
            data = fetch_pokemon_data(pid)
            db.insert_pokemon(data)
            sleep(0.5)
        except Exception as e:
            logging.error(f"Error processing Pokémon ID {pid}: {e}")

    db.close()
    logging.info("ETL process completed")

# Uncomment this if you want to run from CLI
# if __name__ == "__main__":
#     ids_arg = sys.argv[1]
#     pokemon_ids = json.loads(ids_arg)
#     run_etl(pokemon_ids)
