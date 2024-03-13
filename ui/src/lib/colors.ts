import colormap from "colormap";

export function getColorOptions(min: number, max: number, nShades: number = 20): { value: number, color: string }[] {
    let range = max - min;
    let step = range / (nShades - 1);

    let colors: string[] = colormap({
        colormap: "winter",
        nshades: nShades,
        format: "hex",
        alpha: 1,
    });

    return colors.map(
        (color, index) => {
            let value = min + (step * index);
            return { value: value, color: color };
        }
    );
}

export function getFillColor(column: string, colorOptions: { value: number, color: string }[]): any[] {
    return [
        "interpolate",
        ["linear"],
        ["get", column],
        ...colorOptions.flatMap((colorOption) => [
            colorOption.value,
            colorOption.color,
        ]),
    ]
}