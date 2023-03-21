import type { PageLoad } from './$types';
import { PUBLIC_API_URL } from "$env/static/public";
import counties from '$lib/data/california.json';


export const load = (({ fetch }) => {
    const states = fetch(`${PUBLIC_API_URL}/states/`).then(r => r.json());
    console.log(states);

    return {
        counties,
        states
    };

}) satisfies PageLoad;