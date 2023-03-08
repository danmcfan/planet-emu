# Planet Emu
An emulator of the planet Earth.

[Click here to go to the Svelte web application page.](https://planet-emu.com)

[Click here to go to the FastAPI interactive documentation page.](https://api.planet-emu.com)


## Features
- Uses the Google Earth Engine SDK for Python to gather enviornmental attributes from satellite imagery across the contiguous United States
    - Soil (bulk density, water content, pH, clay, sand)
    - Weather (percipitation, temperature, air pressure)
    - Vegetation (normalized difference vegetation index)
- Displays the spatial data in a MapBox web map with controls for selecting different enviornmental attributes
- Accepts user input of coordinates and runs both a simple linear model and two layer deep nueral network model to predict the NDVI for the area immidately surrounding the given coordinates

# Architecture

This full stack application consists of the following:
- REST API backend built using the FastAPI framework in Python
- Web application built using the Svelte framework in Typescript
- PostgreSQL relational database with PostGIS spatial extensions
- Kubernetes cluster to run the application pods and route network traffic
