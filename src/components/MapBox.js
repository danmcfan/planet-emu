import * as React from 'react';
// eslint-disable-next-line import/no-webpack-loader-syntax
import mapboxgl from '!mapbox-gl';

import './MapBox.css';
import { getColorList } from './util';

// const BASE_URL = 'https://api.planet-emu.com';
mapboxgl.accessToken = 'pk.eyJ1IjoiZGFubnktZGFya28iLCJhIjoiY2t1NjRqY2x0MmVnaDJ2b3c5Z3Q3YWJrZSJ9.lShDY5ieeO3Cdr6U_irlVg';

const fillColorProperty = (layer, attribute, depth, summary) => {
    let label;
    if (layer === "soil") {
        label = `${attribute}_${depth}`
    } else {
        label = attribute;
    }

    let colorProperty = ['interpolate',
        ['linear'],
        ['get', label]
    ];
    let colorList = getColorList(layer, attribute, depth, summary);
    for (let item of colorList) {
        colorProperty = colorProperty.concat(item.value, item.color);
    }
    return colorProperty;
};

export default function MapBox(props) {
    const mapContainer = React.useRef(null);
    const map = React.useRef(null);

    React.useEffect(() => {
        if (map.current) return;
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [-97.5, 38],
            zoom: 3
        });
    });

    React.useEffect(() => {
        if (!map.current) return;
        map.current.on('load', () => {
            map.current.addSource('soil', {
                type: 'geojson',
                data: props.counties,
            });

            map.current.addLayer({
                id: 'soil',
                source: 'soil',
                type: 'fill',
                layout: {},
                paint: {
                    'fill-color': fillColorProperty(props.layer, props.attribute, props.depth, props.summary),
                    'fill-opacity': 0.5,
                }
            });

            map.current.addLayer({
                id: 'outline',
                type: 'line',
                source: 'soil',
                layout: {},
                paint: {
                    'line-color': '#000',
                    'line-width': 0.25,
                }
            });

            map.current.on('mouseenter', 'soil', () => {
                map.current.getCanvas().style.cursor = 'pointer';
            });

            // Change it back to a pointer when it leaves.
            map.current.on('mouseleave', 'soil', () => {
                map.current.getCanvas().style.cursor = '';
            });
        });
    });

    React.useEffect(() => {
        if (!map.current) return;
        if (!map.current.getPaintProperty("soil", "fill-color")) return;
        map.current.setPaintProperty("soil", "fill-color", fillColorProperty(props.layer, props.attribute, props.depth, props.summary));
    }, [props.layer, props.attribute, props.depth, props.summary]);

    return (
        <div>
            <div ref={mapContainer} className="map-container" />
        </div>
    );
}