<script lang="ts">
    import type { Choice } from "../types";

    export let choices: Choice[];
    export let selected: Choice;
    export let label: string;

    function handleClick(event: Event) {
        const target = event.target as HTMLElement;
        const value = target.innerText;
        selected = choices.find((choice) => choice.value === value);
    }
</script>

<div class="flex flex-col justify-center">
    <p class="font-bold text-center">{label}</p>
    <div class="flex flex-row justify-center mt-4">
        {#each choices as choice (choice.value)}
            <div
                on:click={handleClick}
                on:keypress={handleClick}
                class="shadow-sm shadow-black rounded-xl w-20 h-14 mx-4 flex justify-center items-center hover:cursor-pointer"
                class:notSelected={selected.value !== choice.value}
                class:selected={selected.value === choice.value}
            >
                <p>{choice.value}</p>
            </div>
        {/each}
    </div>
</div>

<style>
    .notSelected {
        @apply bg-gray-200;
    }

    .selected {
        @apply bg-green-400;
    }
</style>
