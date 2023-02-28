<script>
    let items = [
        { title: "Planet Emu", href: "/" },
        { title: "GitHub", href: "https://github.com/danmcfan" },
    ];
</script>

<div class="h-16 w-auto bg-blue-600 grid grid-cols-2">
    {#each items as item}
        <a
            href={item.href}
            class="flex items-center justify-center text-white font-bold text-2xl hover:cursor-pointer hover:text-gray-300"
        >
            {item.title}
        </a>
    {/each}
</div>

<style>
</style>
