<script lang="ts">
	import '../app.css';
	import NavBar from '../lib/components/NavBar.svelte';
</script>

<div class="w-screen h-screen">
	<NavBar />
	<slot />
</div>
