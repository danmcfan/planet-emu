<script lang="ts">
    import { getContext } from "svelte";
    import { key, mapbox } from "./mapbox";

    const { getMap } = getContext(key);
    const map = getMap();

    export let navigation = "bottom-right";
    export let fullscreen = "bottom-right";
    export let geolocate = "bottom-right";

    map.on("load", () => {
        if (navigation) {
            map.addControl(new mapbox.NavigationControl(), navigation);
        }

        if (fullscreen) {
            map.addControl(new mapbox.FullscreenControl(), fullscreen);
        }

        if (geolocate) {
            map.addControl(new mapbox.GeolocateControl(), geolocate);
        }
    });
</script>
