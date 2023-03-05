<script lang="ts">
    import type { Choice } from "../types";

    export let choices: Choice[];
    export let selected: Choice;

    let value: string = "0";

    $: {
        const index = parseInt(value);
        selected = choices[index];
    }

    $: maxValue = (choices.length - 1).toString();
</script>

<div class="flex flex-col justify-center items-center mt-2">
    <input
        class="w-72 sm:w-96 mt-4 h-2 bg-gray-200 rounded-lg cursor-pointer"
        type="range"
        min="0"
        max={maxValue}
        step="1"
        bind:value
    />
    <div class="flex flex-row space-between">
        <p class="my-2">Depth: {selected.value}</p>
    </div>
</div>
