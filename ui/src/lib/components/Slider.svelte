<script lang="ts">
	export let selectedButtonID: string;
	export let selectedSliderID: string;

	let choices: string[] = ['0', '10', '30', '60', '100', '200'];
	let value: string = '0';

	$: {
		const index = parseInt(value);
		selectedSliderID = choices[index];
	}

	$: maxValue = (choices.length - 1).toString();
</script>

{#if selectedButtonID === 'shovel'}
	<div class="flex flex-col justify-center items-center mt-2">
		<input
			class="w-72 sm:w-96 mt-4 h-2 bg-gray-200 rounded-lg cursor-pointer"
			type="range"
			min="0"
			max={maxValue}
			step="1"
			bind:value
		/>
		<div class="flex flex-row space-between font-mono">
			<p class="my-2 text-[0.75rem]">Depth: {selectedSliderID} cm</p>
		</div>
	</div>
{/if}
