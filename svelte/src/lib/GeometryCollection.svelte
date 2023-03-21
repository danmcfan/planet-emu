<script lang="ts">
    import { getContext } from "svelte";
    import { key, mapbox } from "./mapbox";

    const { getMap } = getContext(key);
    const map = getMap();

    export let source: any;
    export let sourceName: string;
    export let layerName: string;

    export let fillColor: string | any = "white";
    export let fillOpacity = 0.25;

    export let lineColor = "black";
    export let lineWidth = 0.25;

    map.on("load", () => {
        map.addSource(sourceName, {
            type: "geojson",
            data: source,
        });

        map.addLayer({
            id: layerName,
            type: "fill",
            source: sourceName,
            layout: {},
            paint: {
                "fill-color": fillColor,
                "fill-opacity": fillOpacity,
            },
        });

        if (lineColor && lineWidth) {
            map.addLayer({
                id: `${layerName}-outline`,
                type: "line",
                source: sourceName,
                layout: {},
                paint: {
                    "line-color": lineColor,
                    "line-width": lineWidth,
                },
            });
        }
    });

    $: if (map.getLayer(layerName))
        map.setPaintProperty(layerName, "fill-color", fillColor);
</script>
