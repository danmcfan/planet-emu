FROM python:3.10

LABEL org.opencontainers.image.source=https://github.com/danmcfan/planet-emu

WORKDIR /code

ARG DECRYPT_PASSWORD
ENV DECRYPT_PASSWORD=${DECRYPT_PASSWORD}
ARG SQLALCHEMY_DATABASE_URL
ENV SQLALCHEMY_DATABASE_URL=${SQLALCHEMY_DATABASE_URL}

COPY ./service_account.json.gpg /code/service_account.json.gpg
COPY ./scripts/decrypt_secret.sh /code/decrypt_secret.sh

RUN /bin/sh decrypt_secret.sh
RUN cp /root/secrets/service_account.json /code/service_account.json

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./planet_emu/ /code/planet_emu/

CMD ["uvicorn", "planet_emu.api.main:app", "--host", "0.0.0.0", "--port", "80"]
