import colormap from 'colormap';

export const getColorList = (layer, attribute, depth, summary, nBuckets = 8, colormapOption = "winter") => {
    let label;
    if (["bulkdens", "clay", "ph", "sand", "soc", "swc"].includes(attribute)) {
        label = `${attribute}_${depth}`
    } else {
        label = attribute;
    }

    let minValue = summary[label]["min"]
    let maxValue = summary[label]["max"]
    let range = maxValue - minValue;
    let interval = range / nBuckets;
    let colors = colormap({ colormap: colormapOption, nshades: nBuckets, format: "hex", alpha: 1 });

    let colorList = [];
    for (let i = 0; i < nBuckets; i++) {
        colorList.push({ 'value': minValue + (i * interval), 'color': colors[i] });
    }

    return colorList
}