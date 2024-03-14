<script lang="ts">
	import earthSvg from '$lib/icons/earth.svg?raw';
	import githubSvg from '$lib/icons/github.svg?raw';

	const githubLink = 'https://github.com/danmcfan/planet-emu';
</script>

<nav
	class="w-full h-12 flex flex-row justify-between items-center bg-blue-500 shadow-sm shadow-black"
>
	<div class="flex flex-row justify-center items-center mx-4">
		<div class="text-white text-[2rem] mr-4">{@html earthSvg}</div>
		<p class="text-white text-xl font-bold font-mono">Planet Emu</p>
	</div>
	<button
		class="text-white hover:text-gray-200 text-[2rem] mx-4 cursor-pointer"
		on:click={() => {
			window.open(githubLink, '_blank');
		}}
	>
		{@html githubSvg}
	</button>
</nav>
