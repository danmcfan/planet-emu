<script lang="ts">
    import type { Choice } from "../types";

    export let selected: Choice | undefined;
    export let choices: Choice[] = [];
</script>

<div class="flex justify-center">
    <select
        bind:value={selected}
        class="w-5/6 mx-auto text-center border-solid` border-gray-400 border-2 rounded-lg"
    >
        {#each choices as choice}
            <option value={choice}>{choice.value}</option>
        {/each}
    </select>
</div>
