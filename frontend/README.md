# Frontend

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 20.0.0.

## Application Overview

This application allows users to run ETL (Extract, Transform, Load) jobs to load Pokémon data from a REST API into a database. The data is then transformed and made available for users to view within the dataset. Users can filter the Pokémon data by name, type, and ID, making it easy to search and analyze specific Pokémon.

- **ETL Jobs:** Automate the process of fetching, transforming, and storing Pokémon data.
- **Data Source:** Pokémon data is retrieved from a REST API.
- **Database Integration:** Loaded and transformed data is stored in a database for efficient querying.
- **Filtering:** Users can filter Pokémon by name, type, and ID within the application interface.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.


## Building

To build the project run:

```bash
ng build
```