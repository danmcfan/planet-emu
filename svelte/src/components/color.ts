import colormap from "colormap";
import type { ColorOption } from "../types";

export function getColorOptions(values: number[], nShades: number = 10): ColorOption[] {
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


    return colors.map(
        (color, index) => {
            let value = min + (step * index);
            return { value: value, color: color };
        }
    );
}

export function getFillColor(column: string, colorOptions: ColorOption[], opacity: number = 0.8): any[] {
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