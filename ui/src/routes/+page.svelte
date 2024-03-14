<script lang="ts">
	import Map from '$lib/components/Map.svelte';
	import Legend from '$lib/components/Legend.svelte';
	import MapControls from '$lib/components/MapControls.svelte';
	import GeometryCollection from '$lib/components/GeometryCollection.svelte';
	import MapPopup from '$lib/components/MapPopup.svelte';
	import Buttons from '$lib/components/Buttons.svelte';
	import Dropdown from '$lib/components/Dropdown.svelte';
	import Slider from '$lib/components/Slider.svelte';
	import { getColorOptions, getFillColor } from '$lib/colors';

	let fillOpacity = 0.8;
	let geometryCollections = [
		{
			sourceUrl: 'mapbox://danny-darko.d4v2kznn',
			sourceLayer: 'california_25000-dh558w',
			sourceName: 'gridSource_25000',
			layerName: 'gridLayer_25000',
			minZoom: 0,
			maxZoom: 6
		},
		{
			sourceUrl: 'mapbox://danny-darko.945a4o5j',
			sourceLayer: 'california_10000-4u0y3s',
			sourceName: 'gridSource_10000',
			layerName: 'gridLayer_10000',
			minZoom: 6,
			maxZoom: 8
		},
		{
			sourceUrl: 'mapbox://danny-darko.96hf0e0o',
			sourceLayer: 'california_5000-2ku4fl',
			sourceName: 'gridSource_5000',
			layerName: 'gridLayer_5000',
			minZoom: 8,
			maxZoom: 9
		},
		{
			sourceUrl: 'mapbox://danny-darko.dd0wxoom',
			sourceLayer: 'california_2500-9c20ty',
			sourceName: 'gridSource_2500',
			layerName: 'gridLayer_2500',
			minZoom: 9,
			maxZoom: 24
		}
	];

	let selectedButtonID: string = 'shovel';
	let selectedDropdownID: string = 'bulk_density';
	let selectedSliderID: string = '0';

	let column = 'bulk_density_0';
	let [min, max] = [50, 200];

	$: if (selectedButtonID === 'shovel') {
		column = selectedDropdownID + '_' + selectedSliderID;
	} else {
		column = selectedDropdownID;
	}

	$: if (column.startsWith('bulk_density')) {
		[min, max] = [50, 200];
	} else if (column.startsWith('clay')) {
		[min, max] = [0, 50];
	} else if (column.startsWith('ph')) {
		[min, max] = [40, 100];
	} else if (column.startsWith('sand')) {
		[min, max] = [0, 100];
	} else if (column.startsWith('organic_carbon')) {
		[min, max] = [0, 60];
	} else if (column.startsWith('water_content')) {
		[min, max] = [0, 60];
	} else if (column.startsWith('prcp')) {
		[min, max] = [0, 10];
	} else if (column.startsWith('srad')) {
		[min, max] = [200, 600];
	} else if (column.startsWith('swe')) {
		[min, max] = [0, 1500];
	} else if (column.startsWith('tmax')) {
		[min, max] = [-20, 40];
	} else if (column.startsWith('tmin')) {
		[min, max] = [-20, 40];
	} else if (column.startsWith('vp')) {
		[min, max] = [200, 1400];
	} else if (column.startsWith('ndvi')) {
		[min, max] = [0, 0.5];
	}

	$: colorOptions = getColorOptions(min, max);
	$: fillColor = getFillColor(column, colorOptions);

	const getHTML = (e: any) => {
		const [lng, lat] = [e.lngLat.lng.toFixed(2), e.lngLat.lat.toFixed(2)];
		const { properties } = e.features[0];
		let value = Math.round(properties[column] * 100) / 100;

		return `<p style="text-align: center;">(${lng}, ${lat})<br/><b>${value}</b></p>`;
	};
</script>

<div class="flex flex-col justify-center items-center mt-4">
	<Map lng={-120.0} lat={37.5} zoom={4}>
		<Legend {colorOptions} {fillOpacity} />
		<MapControls />
		{#each geometryCollections as geometryCollection (geometryCollection.layerName)}
			<GeometryCollection {...geometryCollection} {fillColor} {fillOpacity} />
			<MapPopup layerName={geometryCollection.layerName} {getHTML} {column} />
		{/each}
	</Map>

	<Buttons bind:selectedButtonID />
	<Dropdown {selectedButtonID} bind:selectedDropdownID />
	<Slider {selectedButtonID} bind:selectedSliderID />
</div>
