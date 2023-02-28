import { publish } from 'gh-pages';

publish(
    "build",
    {
        branch: 'gh-pages',
        repo: 'https://github.com/danmcfan/planet-emu.git',
        user: {
            name: "Danny O'Brien",
            email: "danmcfan33@gmail.com"
        },
        dotfiles: true
    },
    () => {
        console.log("Deploy Complete!");
    }
);