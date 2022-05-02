import * as React from 'react';
import mapboxgl from 'mapbox-gl';

import './MapBox.css';

// const BASE_URL = 'https://api.planet-emu.com';
mapboxgl.accessToken = 'pk.eyJ1IjoiZGFubnktZGFya28iLCJhIjoiY2t1NjRqY2x0MmVnaDJ2b3c5Z3Q3YWJrZSJ9.lShDY5ieeO3Cdr6U_irlVg';

export default function MapBox() {
    const mapContainer = React.useRef(null);
    const map = React.useRef(null);
    const [lng, setLng] = React.useState(-97.5);
    const [lat, setLat] = React.useState(38);
    const [zoom, setZoom] = React.useState(3);

    React.useEffect(() => {
        if (map.current) return;
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [lng, lat],
            zoom: zoom
        });
    });

    React.useEffect(() => {
        if (!map.current) return;
        map.current.on('move', () => {
            setLng(map.current.getCenter().lng.toFixed(4));
            setLat(map.current.getCenter().lat.toFixed(4));
            setZoom(map.current.getZoom().toFixed(2));
        });
    });

    return (
        <div>
            <div className="sidebar">
                Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
            </div>
            <div ref={mapContainer} className="map-container" />
        </div>
    );
}