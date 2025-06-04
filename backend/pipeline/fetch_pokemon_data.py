import requests

from config import BASE_API_URL

def fetch_pokemon_data(pokemon_id):
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
