docker build -t ghcr.io/danmcfan/planet-emu-svelte:latest . \
&& docker push ghcr.io/danmcfan/planet-emu-svelte:latest \
&& kubectl delete pod -l app=static