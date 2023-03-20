<script lang="ts">
    import type { PageData } from "./$types";
    import Map from "$lib/Map.svelte";
    import MapMarker from "$lib/MapMarker.svelte";

    export let data: PageData;
</script>

<div class="h-1/2">
    <Map lng={-100} lat={40} zoom={3}>
        <MapMarker lng={-100} lat={40} label="Hello" />
    </Map>
</div>
