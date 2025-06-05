import strawberry
from typing import Optional
from graphql2.types import Pokemon
from db.queries import get_pokemon_by_id

@strawberry.type
class Query:
    """
    Query class for GraphQL schema.

    This class defines the root query type for the GraphQL API using Strawberry.
    It provides a field to fetch a Pokémon by its unique identifier.

    Methods
    -------
    pokemon(id: int) -> Optional[Pokemon]
        Retrieves a Pokémon object by its ID.
        Parameters:
            id (int): The unique identifier of the Pokémon.
        Returns:
            Optional[Pokemon]: The Pokémon object if found, otherwise None.
    """
    @strawberry.field
    def pokemon(self, id: int) -> Optional[Pokemon]:
        return get_pokemon_by_id(id)

schema = strawberry.Schema(query=Query)
