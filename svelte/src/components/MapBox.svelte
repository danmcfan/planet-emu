<script lang="ts">
    import { onMount, afterUpdate } from "svelte";
    import mapboxgl from "mapbox-gl";

    import { PUBLIC_MAPBOX_TOKEN } from "$env/static/public";
    import california from "$lib/data/california.json";
    import { getPaintProperty } from "./color";

    export let column: string;

    let map: mapboxgl.Map;
    let mapRef: HTMLDivElement;
    let countiesSource = "counties";

    $: values = california.features.map(
        (feature) => feature.properties[column]
    );

    $: paintProperty = getPaintProperty(column, values);

    onMount(async () => {
        mapboxgl.accessToken = PUBLIC_MAPBOX_TOKEN;

        map = new mapboxgl.Map({
            container: mapRef,
            style: "mapbox://styles/mapbox/streets-v11",
            center: [-120.0, 37.5],
            zoom: 4.5,
        });

        map.on("load", () => {
            map.addSource(countiesSource, {
                type: "geojson",
                data: california,
            });

            map.addLayer({
                id: "values",
                type: "fill",
                source: countiesSource,
                layout: {},
                paint: paintProperty,
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

            map.on("mouseenter", "values", () => {
                map.getCanvas().style.cursor = "pointer";
            });

            map.on("mouseleave", "values", () => {
                map.getCanvas().style.cursor = "";
            });
        });
    });

    afterUpdate(() => {
        if (map) {
            map.setPaintProperty(
                "values",
                "fill-color",
                paintProperty["fill-color"]
            );
        }
    });
</script>

<div class="h-4/6 w-auto">
    <div bind:this={mapRef} class="w-full h-full m-0 p-0" />
</div>
