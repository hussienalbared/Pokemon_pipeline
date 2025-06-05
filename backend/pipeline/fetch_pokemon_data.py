import requests

from config import BASE_API_URL

def fetch_pokemon_data(pokemon_id):
    """
    Fetches detailed data for a given Pokémon by its ID, including species and evolution chain information.
    Args:
        pokemon_id (int or str): The ID of the Pokémon to fetch.
    Returns:
        dict: A dictionary containing the following keys:
            - id (int): The Pokémon's ID.
            - name (str): The Pokémon's name.
            - base_experience (int): The base experience gained for defeating this Pokémon.
            - height (int): The Pokémon's height.
            - weight (int): The Pokémon's weight.
            - types (list of str): List of type names associated with the Pokémon.
            - abilities (list of dict): List of abilities, each with:
                - name (str): Ability name.
                - is_hidden (bool): Whether the ability is hidden.
            - stats (list of dict): List of stats, each with:
                - name (str): Stat name.
                - base_stat (int): Base stat value.
                - effort (int): Effort value.
            - evolution_chain_id (int): The ID of the Pokémon's evolution chain.
            - evolution_chain (dict): The evolution chain data structure.
    Raises:
        requests.HTTPError: If any of the API requests fail.
    """
    pokemon_resp = requests.get(f"{BASE_API_URL}/pokemon/{pokemon_id}")
    pokemon_resp.raise_for_status()
    pokemon = pokemon_resp.json()

    species_resp = requests.get(pokemon["species"]["url"])
    species_resp.raise_for_status()
    species = species_resp.json()

    evo_chain_resp = requests.get(species["evolution_chain"]["url"])
    evo_chain_resp.raise_for_status()
    evo_chain = evo_chain_resp.json()

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
