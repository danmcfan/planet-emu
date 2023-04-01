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

<div
    bind:this={container}
    class="w-full h-[20rem] sm:h-[28rem] md:h-[36rem] lg:h-[44rem]"
>
    {#if map}
        <slot />
    {:else}
        <div class="w-full h-full flex justify-center items-center bg-blue-200">
            <p class="text-center text-6xl sm:text-8xl">Loading map...</p>
        </div>
    {/if}
</div>
