FROM node:16 AS build

WORKDIR /code

COPY ./package.json /code/package.json
COPY ./package-lock.json /code/package-lock.json

RUN npm install

COPY ./ /code

RUN npm run build

FROM nginx:alpine

LABEL org.opencontainers.image.source=https://github.com/danmcfan/planet-emu

COPY --from=build /code/build /usr/share/nginx/html