import strawberry
from typing import List

@strawberry.type
class Type:
    id: int
    name: str

@strawberry.type
class Ability:
    id: int
    name: str
    is_hidden: bool

@strawberry.type
class Stat:
    name: str
    base_stat: int
    effort: int

@strawberry.type
class Pokemon:
    """
    Represents a Pokémon entity with its core attributes and related details.

    Attributes:
        id (int): The unique identifier of the Pokémon.
        name (str): The name of the Pokémon.
        base_experience (int): The base experience gained for defeating this Pokémon.
        height (int): The height of the Pokémon in decimetres.
        weight (int): The weight of the Pokémon in hectograms.
        types (List[Type]): A list of types associated with the Pokémon.
        abilities (List[Ability]): A list of abilities the Pokémon can have.
        stats (List[Stat]): A list of statistical attributes for the Pokémon.
    """
    id: int
    name: str
    base_experience: int
    height: int
    weight: int
    types: List[Type]
    abilities: List[Ability]
    stats: List[Stat]
