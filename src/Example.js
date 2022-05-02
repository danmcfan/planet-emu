import * as React from 'react';

export default function Example() {
    const [data, setData] = React.useState(null);

    React.useEffect(() => {
        async function fetchIndex() {
            let response = await fetch("https://api.planet-emu.com/");
            let data = await response.json();
            setData(data.message);
        }
        fetchIndex();
    }, [])

    if (data) {
        return (
            <p>{data}</p>
        );
    } else {
        return (
            <p>Loading...</p>
        );
    }
}