<script lang="ts">
	import { getContext } from 'svelte';
	import { key, mapbox } from '$lib/mapbox';

	const { getMap } = getContext(key);
	const map = getMap();

	export let layerName: string;
	export let getHTML: (e: any) => string;
	export let column: string;

	let popup: mapbox.Popup | null = null;
	let currentColumn: string;

	$: {
		if (currentColumn !== column && popup) {
			popup.remove();
		}
	}

	map.on('load', () => {
		if (map.getLayer(layerName)) {
			map.on('click', layerName, (e: any) => {
				if (popup) {
					popup.remove();
				}
				popup = new mapbox.Popup();
				popup.setLngLat(e.lngLat).setHTML(getHTML(e)).addTo(map);
				currentColumn = column;
			});

			map.on('mouseenter', layerName, () => {
				map.getCanvas().style.cursor = 'pointer';
			});

			map.on('mouseleave', layerName, () => {
				map.getCanvas().style.cursor = '';
			});
		}
	});
</script>
