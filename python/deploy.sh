docker build \
    --build-arg SQLALCHEMY_DATABASE_URL \
    --build-arg GCP_SERVICE_NAME \
    --build-arg GCP_PROJECT \
    --build-arg DECRYPT_PASSWORD \
    -t ghcr.io/danmcfan/planet-emu-fast-api:latest . \
&& docker push ghcr.io/danmcfan/planet-emu-fast-api:latest \
&& kubectl delete pod -l app=api