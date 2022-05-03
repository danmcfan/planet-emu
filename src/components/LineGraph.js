import * as React from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

export default function LineGraph(props) {
    const getData = (layer, featureProperties) => {
        if (featureProperties === null) {
            return null;
        }
        const depths = [0, 10, 30, 60, 100, 200];
        return depths.map(depth => { return { "depth": depth, "value": (featureProperties[`b${depth}_${layer}`]).toFixed(2) } });
    };

    return (
        <LineChart width={600} height={300} data={getData(props.layer, props.featureProperties)} margin={{ top: 10, right: 20, bottom: 10, left: 40 }}>
            <Line type="monotone" dataKey="value" stroke="#1710e0" />
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey="depth" />
            <YAxis domain={["dataMin", "dataMax"]} />
            <Tooltip />
        </LineChart>
    );
}