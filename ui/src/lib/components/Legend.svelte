<script lang="ts">
	export let colorOptions: { value: number; color: string }[];
	export let fillOpacity: number;

	$: minValue = Math.min(...colorOptions.map((option) => option.value));
	$: maxValue = Math.max(...colorOptions.map((option) => option.value));
</script>

<div class="absolute top-0 left-0 m-2 p-2 w-12 flex flex-col rounded-xl bg-white/75">
	<p class="text-[0.5rem] text-center font-bold font-mono">
		{minValue.toFixed(2)}
	</p>
	<div class="flex flex-col justify-center items-center">
		{#each colorOptions as colorOption (colorOption.color)}
			<div class="w-2 h-2">
				<div
					style="background-color: {colorOption.color}; opacity: {fillOpacity};"
					class="w-full h-full"
				/>
			</div>
		{/each}
	</div>
	<p class="text-[0.5rem] text-center font-bold font-mono">
		{maxValue.toFixed(2)}
	</p>
</div>
