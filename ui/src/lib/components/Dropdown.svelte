<script lang="ts">
	export let selectedButtonID: string;
	export let selectedDropdownID: string;

	let choices: { id: string; title: string }[];

	$: if (selectedButtonID === 'shovel') {
		selectedDropdownID = 'bulk_density';
		choices = [
			{ id: 'bulk_density', title: 'Bulk Density (10 * kg / m^3)' },
			{ id: 'clay', title: 'Clay Content (%)' },
			{ id: 'ph', title: 'Soil pH (10 * pH in H2O)' },
			{ id: 'sand', title: 'Sand Content (%)' },
			{ id: 'organic_carbon', title: 'Soil Organic Carbon (5 * g / kg)' },
			{ id: 'water_content', title: 'Soil Water Content (%)' }
		];
	} else if (selectedButtonID === 'cloud') {
		selectedDropdownID = 'prcp';
		choices = [
			{ id: 'prcp', title: 'Percipitation (mm)' },
			{ id: 'srad', title: 'Solar Radiation (W/m^2)' },
			{ id: 'swe', title: 'Snow Water Equivalent (kg / m^2)' },
			{ id: 'tmax', title: 'Maximum Temperature (C)' },
			{ id: 'tmin', title: 'Minimum Temperature (C)' },
			{ id: 'vp', title: 'Water Vapor Pressure (Pa)' }
		];
	} else if (selectedButtonID === 'plant') {
		selectedDropdownID = 'ndvi';
		choices = [{ id: 'ndvi', title: 'NDVI' }];
	}
</script>

<div class="flex flex-col justify-center items-center mt-4">
	<select
		bind:value={selectedDropdownID}
		class="w-72 sm:w-96 mx-auto font-mono text-center text-[0.75rem] border-solid border-gray-400 border-2 rounded-lg"
	>
		{#each choices as choice (choice.id)}
			<option value={choice.id}>{choice.title}</option>
		{/each}
	</select>
</div>
