<script lang="ts">
    import { onMount, afterUpdate } from "svelte";
    import { mapbox } from "./mapbox.ts";

    import { getFillColor } from "../components/legend/color";
    import type { ColorOption } from "../types";

    export let column: string;
    export let colorOptions: ColorOption[];
    export let countyData: any;

    let map: mapbox.Map;
    let mapRef: HTMLDivElement;
    let countiesSource = "counties";

    $: fillColor = getFillColor(column, colorOptions);

    onMount(async () => {
        map = new mapbox.Map({
            container: mapRef,
            style: "mapbox://styles/mapbox/streets-v11",
            center: [-120.0, 37.5],
            zoom: 4,
            attributionControl: false,
        });

        map.on("load", () => {
            map.addSource(countiesSource, {
                type: "geojson",
                data: countyData,
            });

            map.addLayer({
                id: "values",
                type: "fill",
                source: countiesSource,
                layout: {},
                paint: {
                    "fill-color": fillColor,
                    "fill-opacity": 0.75,
                },
            });

            map.addLayer({
                id: "outline",
                type: "line",
                source: countiesSource,
                layout: {},
                paint: {
                    "line-color": "#000",
                    "line-width": 0.25,
                },
            });

            map.on("click", "values", (e) => {
                const { properties } = e.features[0];
                const { county_name, state_name } = properties;
                const value = Math.round(properties[column] * 100) / 100;

                const popup = new mapboxgl.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(
                        `<h3>${county_name}, ${state_name}</h3><p><b>${value}</b></p>`
                    )
                    .addTo(map);
            });

            map.on("mouseenter", "values", () => {
                map.getCanvas().style.cursor = "pointer";
            });

            map.on("mouseleave", "values", () => {
                map.getCanvas().style.cursor = "";
            });

            map.addControl(new mapbox.NavigationControl(), "bottom-right");
            map.addControl(new mapbox.FullscreenControl(), "bottom-right");
            map.addControl(new mapbox.GeolocateControl(), "bottom-right");
        });
    });

    afterUpdate(() => {
        if (map) {
            map.setPaintProperty("values", "fill-color", fillColor);
        }
    });
</script>

<div
    class="h-[20rem] sm:h-[28rem] w-auto border-b-[0.1rem] border-black border-solid"
>
    <div bind:this={mapRef} class="w-full h-full m-0 p-0" />
</div>
