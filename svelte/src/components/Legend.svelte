<script lang="ts">
    import type { ColorOption } from "../types";

    export let colorOptions: ColorOption[];
</script>

<div class="flex flex-row justify-between w-4/6">
    {#each colorOptions as colorOption (colorOption.color)}
        <div class="flex flex-col items-center">
            <p class="font-bold text-lg">
                {Math.round(colorOption.value * 100) / 100}
            </p>
            <div
                style="background-color: {colorOption.color}"
                class="w-12 h-12"
            />
        </div>
    {/each}
</div>
