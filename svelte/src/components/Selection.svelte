<script lang="ts">
    import "iconify-icon";
    import type { Choice } from "../types";

    export let choices: Choice[];
    export let selected: Choice;
    export let label: string;

    function handleClick(event: Event) {
        const target = event.target as HTMLElement;
        const id = target.id;
        if (id) {
            selected = choices.find((choice) => choice.id === id);
        }
    }
</script>

<div class="flex flex-row justify-center mt-6">
    {#each choices as choice (choice.id)}
        <div class="flex flex-col justify-center items-center">
            <div
                id={choice.id}
                on:click={handleClick}
                on:keypress={handleClick}
                class="bg-gray-200 hover:bg-gray-400 hover:cursor-pointer w-16 h-16 mx-6 rounded-lg flex justify-center items-center shadow-sm shadow-black"
                class:selected={selected.id === choice.id}
            >
                <iconify-icon
                    id={choice.id}
                    icon={choice.icon}
                    class="text-black text-[2.25rem]"
                />
            </div>
            <p class="text-xs mt-1">{choice.value}</p>
        </div>
    {/each}
</div>

<style>
    .selected {
        @apply bg-green-600;
    }
</style>
