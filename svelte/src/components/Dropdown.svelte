<script lang="ts">
    import type { Choice } from "../types";

    export let selected: Choice | undefined;
    export let choices: Choice[] = [];
    export let label: string = "";
</script>

<div class="flex flex-col content-center">
    <p class="font-bold text-center mb-4">{label}</p>
    <select
        bind:value={selected}
        class="w-5/6 mx-auto text-center border-solid` border-gray-400 border-2 rounded-lg"
    >
        {#each choices as choice}
            <option value={choice}>{choice.value}</option>
        {/each}
    </select>
</div>
