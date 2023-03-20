<script lang="ts">
    import { getContext } from "svelte";
    import { key } from "./mapbox";

    const { getMap } = getContext(key);
    const map = getMap();

    export let source: any;
    export let sourceName = "sourceName";
    export let layerName = "layerName";

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
            "fill-color": "#000",
            "fill-opacity": 0.75,
        },
    });
</script>
