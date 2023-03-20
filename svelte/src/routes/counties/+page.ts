import type { PageLoad } from './$types';

export const load = (async ({ fetch, params }) => {
    let counties = await fetch(`http://localhost:8000/counties/geojson?state_name=California`).then(r => r.json());

    return {
        counties
    };
}) satisfies PageLoad;