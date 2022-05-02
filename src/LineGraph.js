import * as React from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

export default function LineGraph() {
    const data = [
        { "depth": 0, "bulkdens": 150 },
        { "depth": 10, "bulkdens": 160 },
        { "depth": 30, "bulkdens": 162 },
        { "depth": 60, "bulkdens": 167 },
        { "depth": 100, "bulkdens": 172 },
        { "depth": 200, "bulkdens": 175 },
    ]

    return (
        <LineChart width={600} height={300} data={data} margin={{ top: 10, right: 20, bottom: 10, left: 40 }}>
            <Line type="monotone" dataKey="bulkdens" stroke="#000000" />
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey="depth" />
            <YAxis domain={[145, 180]} />
            <Tooltip />
        </LineChart>
    );
}