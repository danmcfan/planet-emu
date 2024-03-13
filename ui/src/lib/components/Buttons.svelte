<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import shovelSvg from '$lib/icons/shovel.svg?raw';
	import cloudSvg from '$lib/icons/cloud.svg?raw';
	import plantSvg from '$lib/icons/plant.svg?raw';

	const symbols = [
		{ id: 'shovel', svg: shovelSvg, tooltip: 'Soil' },
		{ id: 'cloud', svg: cloudSvg, tooltip: 'Weather' },
		{ id: 'plant', svg: plantSvg, tooltip: 'Vegetation' }
	];

	export let selectedButtonID = 'shovel';

	function handleClick(id: string) {
		selectedButtonID = id;
	}
</script>

<div class="w-full flex flex-row justify-center items-center my-4">
	{#each symbols as symbol (symbol.id)}
		<Button
			selected={symbol.id === selectedButtonID}
			svg={symbol.svg}
			tooltip={symbol.tooltip}
			onClick={() => handleClick(symbol.id)}
		/>
	{/each}
</div>
