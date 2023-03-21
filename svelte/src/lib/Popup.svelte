<script lang="ts">
    import { getContext } from "svelte";
    import { key, mapbox } from "./mapbox";

    const { getMap } = getContext(key);
    const map = getMap();

    export let layerName: string;
    export let getHTML: (e: any) => string;

    map.on("load", () => {
        if (map.getLayer(layerName)) {
            map.on("click", layerName, (e: any) => {
                new mapbox.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(getHTML(e))
                    .addTo(map);
            });

            map.on("mouseenter", layerName, () => {
                map.getCanvas().style.cursor = "pointer";
            });

            map.on("mouseleave", layerName, () => {
                map.getCanvas().style.cursor = "";
            });
        }
    });
</script>
