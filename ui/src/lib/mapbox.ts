import mapbox from 'mapbox-gl';

import { env } from "$env/dynamic/public";

mapbox.accessToken = env.PUBLIC_MAPBOX_TOKEN;

const key = Symbol();

export { mapbox, key };