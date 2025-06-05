import os
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
    """
    Runs the ETL (Extract, Transform, Load) process for a list of Pokémon IDs.
    This function creates the necessary database directory, initializes the Pokémon database,
    and processes each Pokémon ID by fetching its data and inserting it into the database.
    Logs are generated for each step, and errors are handled gracefully.
    Args:
        pokemon_ids (list): A list of Pokémon IDs (integers) to process.
    Raises:
        Any exceptions raised during data fetching or database insertion are logged but not propagated.
    Side Effects:
        - Creates the database directory if it does not exist.
        - Inserts Pokémon data into the database.
        - Writes log messages to the logging system.
        - Sleeps for 0.5 seconds between processing each Pokémon ID.
    """
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
