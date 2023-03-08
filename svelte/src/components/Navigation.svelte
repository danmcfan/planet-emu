<script lang="ts">
    import Icon from "@iconify/svelte";

    const apiLink = "https://api.planet-emu.com/docs";
    const githubLink = "https://github.com/danmcfan/planet-emu";
</script>

<div
    class="h-12 w-full sm:h-16
           relative flex flex-row justify-between items-center
           bg-blue-600 border-b-[0.1rem] border-black border-solid"
>
    <div class="flex flex-row justify-center items-center mx-4 sm:mx-8 ">
        <iconify-icon
            icon="ri:earth-fill"
            class="text-white  text-[2rem] sm:text-[2.5rem]"
        />
        <div class="text-white font-bold text-xl sm:text-2xl ml-4">
            Planet Emu
        </div>
    </div>
    <div class="flex flow-row justify-around items-center">
        <a
            class="group mx-4 sm:mx-8 flex flex-row justify-center items-center hover:cursor-pointer"
            href={apiLink}
        >
            <Icon
                icon="simple-icons:fastapi"
                class="text-white group-hover:text-black text-[1.75rem] sm:text-[2.25rem]"
            />
        </a>
        <a
            class="group mx-4 sm:mx-8 flex flex-row justify-center items-center hover:cursor-pointer"
            href={githubLink}
        >
            <Icon
                icon="carbon:logo-github"
                class="text-white group-hover:text-black text-[2rem] sm:text-[2.5rem]"
            />
        </a>
    </div>
</div>

<style>
</style>
