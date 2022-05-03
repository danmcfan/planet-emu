# planet-emu
A geospatial data processing library built using Google Earth Engine API for Python.

## GitHub Pages
[Click here](https://danmcfan.github.io/planet-emu) for the GitHub Pages frontend web application.

## Features
- Executes geospatial queries to Google Earth Engine using AWS Lambda Functions.
    - Gathers soil, weather, and spectral properties for county boundaries within the contiguous United States.
- Deploys a JavaScript React web application to GitHub Pages.
    - Displays the geospatial data as layers within a MapBox component.
- Creates a simple regression model using TensorFlow to predict the relationship between weather / soil and the normalized difference vegetation index (NDVI).

## Architecture
![Architecture](docs/architecture.png)
