<script lang="ts">
    import { onMount, onDestroy, setContext } from "svelte";
    import { mapbox, key } from "./mapbox";

    setContext(key, {
        getMap: () => map,
    });

    export let lng: number;
    export let lat: number;
    export let zoom: number;

    let container: HTMLDivElement;
    let map: mapboxgl.Map;

    onMount(() => {
        map = new mapbox.Map({
            container,
            style: "mapbox://styles/mapbox/streets-v11",
            center: [lng, lat],
            zoom,
            attributionControl: false,
        });
    });

    onDestroy(() => {
        if (map) map.remove();
    });
</script>

<svelte:head>
    <link
        href="https://api.mapbox.com/mapbox-gl-js/v2.13.0/mapbox-gl.css"
        rel="stylesheet"
    />
</svelte:head>

<div bind:this={container} class="w-full h-full">
    {#if map}
        <slot />
    {:else}
        <div class="text-center text-4xl mt-8">Loading map...</div>
    {/if}
</div>
