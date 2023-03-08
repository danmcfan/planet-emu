docker build \
    --build-arg DECRYPT_PASSWORD \
    --build-arg SQLALCHEMY_DATABASE_URL \
    -t ghcr.io/danmcfan/planet-emu-fast-api:latest . \
&& docker push ghcr.io/danmcfan/planet-emu-fast-api:latest