<script lang="ts">
    import type { ColorOption } from "../../types";

    export let colorOptions: ColorOption[];

    $: minValue = Math.min(...colorOptions.map((option) => option.value));
    $: maxValue = Math.max(...colorOptions.map((option) => option.value));
</script>

<div
    class="flex flex-row justify-center items-center h-8 border-solid border-black border-b-2"
>
    <p class="text-sm text-center font-bold w-20 mx-4">
        {minValue.toFixed(2)}
    </p>
    <div class="flex flex-row justify-center">
        {#each colorOptions as colorOption (colorOption.color)}
            <div
                class="w-8 h-4 border-black border-solid border-2 border-l-0 first:border-l-2"
            >
                <div
                    style="background-color: {colorOption.color}; opacity: 0.75;"
                    class="w-full h-full"
                />
            </div>
        {/each}
    </div>
    <p class="text-sm text-center font-bold w-20 mx-4">
        {maxValue.toFixed(2)}
    </p>
</div>
