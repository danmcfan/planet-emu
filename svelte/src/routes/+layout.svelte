<script>
	import "../app.css";
	import Navigation from "../components/Navigation.svelte";
</script>

<head>
	<title>Planet Emu</title>
</head>

<div class="h-screen w-screen flex flex-col">
	<Navigation />
	<slot />
</div>
