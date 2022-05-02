import * as React from 'react';

export default function Example() {
    const [data, setData] = React.useState(null);

    React.useEffect(() => {
        async function fetchIndex() {
            let response = await fetch("https://api.planet-emu.com/mirror/Hello World");
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