<script lang="ts">
	export let selected: boolean = false;
	export let svg: string;
	export let tooltip: string = '';
	export let onClick: () => void;

	$: selectedClasses = selected ? 'bg-blue-500 hover:bg-blue-700' : 'bg-gray-200 hover:bg-gray-400';
</script>

<button
	class="{selectedClasses} group relative flex justify-center items-center w-16 h-16 mx-4 rounded-lg shadow-sm shadow-black text-black text-[2rem]"
	on:click={onClick}
>
	{@html svg}
	<span
		class="absolute top-full left-1/2 transform -translate-x-1/2 px-2 py-1 text-black font-mono text-[0.75rem] opacity-0 transition-opacity duration-300 group-hover:opacity-100"
	>
		{tooltip}
	</span>
</button>
