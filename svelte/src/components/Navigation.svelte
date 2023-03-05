<script lang="ts">
    import "iconify-icon";

    const githubLink = "https://github.com/danmcfan/planet-emu";
</script>

<div
    class="h-12 w-full sm:h-16
           relative flex flex-row justify-between items-center
           bg-blue-600 border-b-[0.1rem] border-black border-solid"
>
    <div
        class="group flex flex-row justify-center items-center mx-4 sm:mx-8 hover:cursor-pointer"
    >
        <iconify-icon
            icon="ri:earth-fill"
            class="text-white group-hover:text-black text-[2rem] sm:text-[2.5rem]"
        />
        <div
            class="text-white group-hover:text-black font-bold text-xl sm:text-2xl ml-4"
        >
            Planet Emu
        </div>
    </div>
    <a
        class="group mx-4 sm:mx-8 flex flex-row justify-center items-center hover:cursor-pointer"
        href={githubLink}
    >
        <iconify-icon
            icon="mdi:github"
            class="text-white group-hover:text-black text-[2rem] sm:text-[2.5rem]"
        />
    </a>
</div>

<style>
</style>
