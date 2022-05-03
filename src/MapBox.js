import * as React from 'react';
import mapboxgl from 'mapbox-gl';

import './MapBox.css';
import counties_geojson from './data/bulkdens.geojson';

// const BASE_URL = 'https://api.planet-emu.com';
mapboxgl.accessToken = 'pk.eyJ1IjoiZGFubnktZGFya28iLCJhIjoiY2t1NjRqY2x0MmVnaDJ2b3c5Z3Q3YWJrZSJ9.lShDY5ieeO3Cdr6U_irlVg';

export default function MapBox() {
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
            map.current.addSource('counties', {
                type: 'geojson',
                data: counties_geojson,
            });

            map.current.addLayer({
                id: 'counties',
                source: 'counties',
                type: 'fill',
                layout: {},
                paint: {
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'b0_mean'],
                        120, "#fdfefe",
                        130, "#fadbd8",
                        140, "#f1948a",
                        150, "#e74c3c",
                        160, "#b03a2e",
                        170, "#78281f",
                    ],
                    'fill-opacity': 0.5,
                }
            });

            map.current.addLayer({
                id: 'outline',
                type: 'line',
                source: 'counties',
                layout: {},
                paint: {
                    'line-color': '#000',
                    'line-width': 0.25,
                }
            });
        });
    });

    return (
        <div>
            <div ref={mapContainer} className="map-container" />
        </div>
    );
}