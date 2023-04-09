# Planet Emu

[Click here to go to the Svelte web application page.](https://planet-emu.com)

[Click here to go to the FastAPI interactive documentation page.](https://api.planet-emu.com)

# Overview

## Google Earth Engine Data Ingestion

- Gathers information using Google Earth Engine SDK for Python
- The 6 soil images have no temporal dimension, so it is just a single image
- The weather and spectral image collections have a temporal dimension, but they are averaged across this dimension to reduce them to a single image
    - Soil Images = bulk density, water content, organic carbon, clay, sand, pH
    - Weather Image Collection = percipitation, maximum temperature, minimum temperature, vapor pressure, solar radiation
    - Spectral Image Collection = NDVI (normalized difference vegetation index)
        - calculated using the RED and NIR (near infrared) bands of the spectral image collection
        - NDVI = ( NIR - RED ) / ( NIR + RED )
- Gathers data across the spatial boundary of California
    - There are computational limits for the public API to Google Earth Engine, so a single state was chosen to reduce ingestion time
- Gathers data as a square grid at five resolutions (25k, 10k, 5k, 2.5k, 1k)

## Svelte Frontend with MapBox

- The combined grid datasets for four of the five resolutions are stored in MapBox as tilesets
- These tilesets are served to the frontend through the MapBox JavaScript SDK
- Each tileset is activated at different zoom levels to reduce the amount of data being streamed to the client
- Different properties of the tilesets can be displayed by using the controls below the map

## TensorFlow Neural Network Model

- The 1k resolution grid dataset is used to train the neural network
- The soil and weather properties are used as input parameters and the NDVI property is used as the ouptut parameter
- The neural network has three layers with 1024, 512, and 256 nodes with two 20% dropout layers between the node layers
- Using 1000 epochs of training, the neural network can reach a mean squared error of 3.00e-4 meaning the predicted value is within 0.0173 of the actual value on average
- The NDVI values within the dataset range from 0.01 to 0.50
- The model can be tested with different input values using the prediction component on the frontend application

# Architecture

## FastAPI REST API

- REST API to serve as an intermediary between the Svelte frontend, Celery worker, and PostgreSQL database
- Accepts POST to make model prediction jobs
- Accepts GET to retrieve model predictions from completed jobs

## Celery Worker

- Generates model predictions using the pretrained neural network
- Saves these results to the PostgreSQL database

## Svelte Frontend

- Displays the MapBox tilesets of the California grids ingested from Google Earth Engine
- Allows toggling of the displayed properties of the tilesets using buttons and dropdowns
- Sends POST requests for model predictions using the form and displays the results

## PostgreSQL Database

- Stores model prediction job results

## Kubernetes Cluster

- Runs the FastAPI REST API, Celery worker, and Svelte frontend deployments
- Handles the network traffic to each of the deployment services
