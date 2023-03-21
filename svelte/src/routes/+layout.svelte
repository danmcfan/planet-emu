<script>
	import "../app.css";
	import Navigation from "$lib/Navigation.svelte";
</script>

<head>
	<title>Planet Emu</title>
</head>

<div class="h-full w-full flex flex-col">
	<Navigation />
	<slot />
</div>
