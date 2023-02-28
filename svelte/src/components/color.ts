import colormap from "colormap";

export type ColorOption = {
    value: number;
    color: string;
};

export function getPaintProperty(column: string, values: number[], nShades: number = 10, opacity: number = 0.8) {
    let min = Math.min(...values);
    let max = Math.max(...values);

    let range = max - min;
    let step = range / nShades;

    let colors: string[] = colormap({
        colormap: "winter",
        nshades: nShades,
        format: "hex",
        alpha: 1,
    });


    let colorOptions: ColorOption[] = colors.map(
        (color, index) => {
            let value = min + (step * index);
            return { value: value, color: color };
        }
    );

    return {
        "fill-color": [
            "interpolate",
            ["linear"],
            ["get", column],
            ...colorOptions.flatMap((colorOption) => [
                colorOption.value,
                colorOption.color,
            ]),
        ],
        "fill-opacity": opacity,
    };
}