<script lang="ts">
    import type { Choice } from "../types";

    export let selected: Choice | undefined;
    export let choices: Choice[] = [];
</script>

<div class="flex flex-col content-center mt-4">
    <select
        bind:value={selected}
        class="w-72 sm:w-96 mx-auto text-center border-solid` border-gray-400 border-2 rounded-lg"
    >
        {#each choices as choice}
            <option value={choice}>{choice.value}</option>
        {/each}
    </select>
</div>
