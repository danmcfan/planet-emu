import colormap from 'colormap';

export const getColorList = (layer, soilSummary, nBuckets = 6, colormapOption = 'winter') => {
    let minValue = soilSummary[layer]["min"]
    let maxValue = soilSummary[layer]["max"]
    let range = maxValue - minValue;
    let interval = range / nBuckets;
    let colors = colormap({ colormap: colormapOption, nshades: nBuckets, format: "hex", alpha: 1 });

    let colorList = [];
    for (let i = 0; i < nBuckets; i++) {
        colorList.push({ 'value': minValue + (i * interval), 'color': colors[i] });
    }

    return colorList
}