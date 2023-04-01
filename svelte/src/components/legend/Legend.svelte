<script lang="ts">
    import type { ColorOption } from "../../types";

    export let colorOptions: ColorOption[];
    export let fillOpacity: number;

    $: minValue = Math.min(...colorOptions.map((option) => option.value));
    $: maxValue = Math.max(...colorOptions.map((option) => option.value));
</script>

<div
    class="flex flex-row justify-center items-center h-8 sm:h-12 border-solid border-black border-b-[0.1rem]"
>
    <p class="text-sm sm:text-base text-center font-bold w-20 mx-4">
        {minValue.toFixed(2)}
    </p>
    <div class="flex flex-row justify-center">
        {#each colorOptions as colorOption (colorOption.color)}
            <div
                class="w-[0.5rem] sm:w-[1rem] h-4 sm:h-6 border-black border-solid border-[0.1rem] border-l-0 first:border-l-[0.1rem]"
            >
                <div
                    style="background-color: {colorOption.color}; opacity: {fillOpacity};"
                    class="w-full h-full"
                />
            </div>
        {/each}
    </div>
    <p class="text-sm sm:text-base text-center font-bold w-20 mx-4">
        {maxValue.toFixed(2)}
    </p>
</div>
