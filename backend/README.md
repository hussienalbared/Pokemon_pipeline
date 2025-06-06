# 🧠 Pokemon Data API

A backend project for managing and querying Pokémon data using GraphQL and RESTful APIs. It features ETL pipelines, a structured database, and containerized deployment with Docker.

## 📁 Project Structure

```
backend
├── Dockerfile                 # Containerization config
├── README.md                  # Project documentation
├── config.py                  # Configuration settings
├── data
│   └── pokemon.db             # SQLite database
├── db                         # Database layer
│   ├── __init__.py
│   ├── base.py                # utilities database functions
│   ├── models.py              # DB Sqlite management
│   ├── queries.py             # Custom DB queries
│   └── schema.py              # DB schema definition
├── graphql2                   # GraphQL schema and types
│   ├── __init__.py
│   ├── schema.py              # GraphQL schema
│   └── types.py               # GraphQL object types
├── logs
│   └── etl.log                # ETL pipeline logs
├── pipeline                   # ETL jobs
│   ├── __init__.py
│   ├── etl_job.py             # Orchestrates ETL flow
│   └── fetch_pokemon_data.py  # Data fetching logic
├── requirements.txt           # Python dependencies
├── routes                     # API routes
│   ├── __init__.py
│   ├── etl_routes.py          # ETL route handlers
│   ├── filter_routes.py       # Filtering logic
│   ├── index_routes.py        # Root/index routes
│   └── pokemon_routes.py      # Pokémon-specific endpoints
└── server.py                  # App entry point
```

## 🚀 Getting Started

### 1. Set Up the Environment

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python server.py
```

The API will be available at `http://localhost:8000`.

### 3. Run with Docker

```bash
docker build -t pokemon-api .
docker run -p 8000:8000 pokemon-api
```

## 🔧 Features

* REST and GraphQL API support
* ETL pipeline for importing Pokémon data
* SQLite for local data persistence
* Modular and scalable project structure

## 🧩 Using the GraphQL API

The GraphQL endpoint is available at `/graphql`.

**Example Query:**

```graphql
query {
    {
     pokemon(id: 10) {
        id
        name
        weight
        types {
            id
            name
        }
  }
}
}
```

**Example Response:**

```json
{
  "data": {
    "pokemon": {
      "id": 10,
      "name": "caterpie",
      "weight": 29,
      "types": [
        {
          "id": 6,
          "name": "bug"
        }
      ]
    }
  }
}
```

## 📌 Notes

* Default database: `data/pokemon.db`
* Log files for ETL stored in `logs/etl.log`

## 📬 License

MIT License – feel free to use and modify.

---
