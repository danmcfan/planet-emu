import * as React from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

export default function LineGraph() {
    const raw_data = require("./data/bulkdens.json")
    const data = raw_data.map(x => {
        x.bulkdens = x.bulkdens.toFixed(2);
        return x;
    })

    return (
        <LineChart width={600} height={300} data={data} margin={{ top: 10, right: 20, bottom: 10, left: 40 }}>
            <Line type="monotone" dataKey="bulkdens" stroke="#000000" />
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey="depth" />
            <YAxis domain={[140, 180]} />
            <Tooltip />
        </LineChart>
    );
}