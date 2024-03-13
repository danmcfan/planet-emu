<script lang="ts">
	import { getContext } from 'svelte';
	import { key } from '$lib/mapbox';

	const { getMap } = getContext(key);
	const map = getMap();

	export let sourceUrl: string;
	export let sourceLayer: string;

	export let sourceName: string;
	export let layerName: string;

	export let fillColor: string | any = 'white';
	export let fillOpacity = 0.75;

	export let minZoom = 0;
	export let maxZoom = 24;

	map.on('load', () => {
		map.addSource(sourceName, {
			type: 'vector',
			url: sourceUrl
		});

		map.addLayer({
			id: layerName,
			type: 'fill',
			source: sourceName,
			'source-layer': sourceLayer,
			layout: {},
			paint: {
				'fill-color': fillColor,
				'fill-opacity': fillOpacity
			},
			minzoom: minZoom,
			maxzoom: maxZoom
		});
	});

	$: if (map.getLayer(layerName)) map.setPaintProperty(layerName, 'fill-color', fillColor);
</script>
