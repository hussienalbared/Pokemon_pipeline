# import sqlite3
# import graphene

# DB_PATH = "data/pokemon.db"

# class PokemonType(graphene.ObjectType):
#     id = graphene.Int()
#     name = graphene.String()
#     base_experience = graphene.Int()
#     height = graphene.Int()
#     weight = graphene.Int()
#     types = graphene.List(graphene.String)
#     abilities = graphene.List(graphene.String)

#     def resolve_types(self, info):
#         with sqlite3.connect(DB_PATH) as conn:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 SELECT t.name FROM Type t
#                 JOIN PokemonType pt ON pt.type_id = t.id
#                 WHERE pt.pokemon_id = ?
#             """, (self.id,))
#             return [row[0] for row in cursor.fetchall()]

#     def resolve_abilities(self, info):
#         with sqlite3.connect(DB_PATH) as conn:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 SELECT a.name FROM Ability a
#                 JOIN PokemonAbility pa ON pa.ability_id = a.id
#                 WHERE pa.pokemon_id = ?
#             """, (self.id,))
#             return [row[0] for row in cursor.fetchall()]

# class Query(graphene.ObjectType):
#     pokemons = graphene.List(
#         PokemonType,
#         name=graphene.String(),
#         type=graphene.String(),
#         ability=graphene.String()
#     )

#     def resolve_pokemons(self, info, name=None, type=None, ability=None):
#         conn = sqlite3.connect(DB_PATH)
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()

#         query = """
#             SELECT DISTINCT p.id, p.name, p.base_experience, p.height, p.weight
#             FROM Pokemon p
#             LEFT JOIN PokemonType pt ON p.id = pt.pokemon_id
#             LEFT JOIN Type t ON pt.type_id = t.id
#             LEFT JOIN PokemonAbility pa ON p.id = pa.pokemon_id
#             LEFT JOIN Ability a ON pa.ability_id = a.id
#             WHERE 1=1
#         """
#         params = []
#         if name:
#             query += " AND LOWER(p.name) LIKE ?"
#             params.append(f"%{name.lower()}%")
#         if type:
#             query += " AND LOWER(t.name) = ?"
#             params.append(type.lower())
#         if ability:
#             query += " AND LOWER(a.name) = ?"
#             params.append(ability.lower())

#         cursor.execute(query, params)
#         rows = cursor.fetchall()
#         return [PokemonType(**dict(row)) for row in rows]

# schema = graphene.Schema(query=Query)
