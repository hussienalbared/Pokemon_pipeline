
# Pokémon Project

This project is a Pokémon-themed web application that enables users to explore, search, and interact with comprehensive Pokémon data. It is designed for Pokémon enthusiasts and developers interested in learning about web development with real-world data.

## Features

- **Browse Pokémon:** View a list of Pokémon with basic info.
- **Detailed Pokémon Info:** See abilities, types, and stats.
- **Search Functionality:** Search by name, ID, or filter by type.
- **API Integration:** Fetches live data from the public PokéAPI.

## Installation

### Clone the repository:

   ```bash
   git clone https://github.com/hussienalbared/Pokemon_pipeline.git
   cd Pokemon_pipeline
````

### Run Docker Compose:

   ```bash
   docker-compose up --build
   ```

   This will:

   * Start the **frontend (Angular)** at: [http://localhost:4000](http://localhost:4000)
   * Start the **backend (Flask API)** at: [http://localhost:8000](http://localhost:8000)

## Project Structure

```text
pokemon
├── README.md
├── backend
│   ├── Dockerfile
│   ├── config.py
│   ├── data/
│   ├── db/
│   ├── logs/
│   ├── pipeline/
│   ├── requirements.txt
│   ├── routes/
│   └── server.py
├── docker-compose.yml
├── frontend/
└── project_tree.py
```

## 🛠️ Technologies Used

* **Angular** – Frontend framework
* **TypeScript** – Angular’s language
* **Flask** – Backend web APIs
* **Docker + Docker Compose** – Deployment & orchestration
* **SQLite** – (or PostgreSQL) as database
* **[PokéAPI](https://pokeapi.co/)** – Pokémon data source

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

