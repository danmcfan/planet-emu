<script lang="ts">
    import MapBox from "../components/MapBox.svelte";
    import Dropdown from "../components/Dropdown.svelte";
    import Legend from "../components/Legend.svelte";

    import { getColorOptions } from "../components/color";
    import type { Choice } from "../types";
    import countyData from "$lib/data/california.json";

    const layerChoices: Choice[] = [
        { id: "soil", value: "Soil" },
        { id: "weather", value: "Weather" },
        { id: "ndvi", value: "NDVI" },
    ];

    const soilAttributeChoices: Choice[] = [
        { id: "bulkdens", value: "Bulk Density (10 * kg / m^3)" },
        { id: "clay", value: "Clay Content (%)" },
        { id: "ph", value: "Soil pH (10 * pH in H2O)" },
        { id: "sand", value: "Sand Content (%)" },
        { id: "soc", value: "Soil Organic Carbon (5 * g / kg)" },
        { id: "swc", value: "Soil Water Content (%)" },
    ];

    const weatherAttributeChoices: Choice[] = [
        { id: "dayl", value: "Day Length (s)" },
        { id: "prcp", value: "Percipitation (mm)" },
        { id: "srad", value: "Solar Radiation (W/m^2)" },
        { id: "swe", value: "Snow Water Equivalent (kg / m^2)" },
        { id: "tmax", value: "Maximum Temperature (C)" },
        { id: "tmin", value: "Minimum Temperature (C)" },
        { id: "vp", value: "Water Vapor Pressure (Pa)" },
    ];

    const ndviAttributeChoices: Choice[] = [
        { id: "ndvi", value: "True NDVI" },
        { id: "linear_ndvi", value: "Linear Model NDVI" },
        { id: "dnn_ndvi", value: "DNN Model NDVI" },
    ];

    const depthChoices: Choice[] = [
        { id: "0", value: "0 cm" },
        { id: "10", value: "10 cm" },
        { id: "30", value: "30 cm" },
        { id: "60", value: "60 cm" },
        { id: "100", value: "100 cm" },
        { id: "200", value: "200 cm" },
    ];

    let layer: Choice = layerChoices[0];
    let soilAttribute: Choice = soilAttributeChoices[0];
    let weatherAttribute: Choice = weatherAttributeChoices[0];
    let ndviAttribute: Choice = ndviAttributeChoices[0];
    let depth: Choice = depthChoices[0];

    function getColumn(
        layer: Choice,
        soilAttribute: Choice,
        weatherAttribute: Choice,
        ndviAttribute: Choice,
        depth: Choice
    ): string {
        if (layer.id === "soil") {
            return soilAttribute.id + "_" + depth.id;
        } else if (layer.id === "weather") {
            return weatherAttribute.id;
        } else if (layer.id === "ndvi") {
            return ndviAttribute.id;
        }
        return "bulkdens_0";
    }

    $: column = getColumn(
        layer,
        soilAttribute,
        weatherAttribute,
        ndviAttribute,
        depth
    );

    $: values = countyData.features.map(
        (feature) => feature.properties[column]
    );
    $: colorOptions = getColorOptions(values);
</script>

<MapBox {column} {colorOptions} {countyData} />

<div class="grid grid-cols-3 justify-between mt-1">
    <Dropdown bind:selected={layer} choices={layerChoices} label="Layer" />
    {#if layer.id === "soil"}
        <Dropdown
            bind:selected={soilAttribute}
            choices={soilAttributeChoices}
            label="Attribute"
        />
        <Dropdown bind:selected={depth} choices={depthChoices} label="Depth" />
    {:else if layer.id === "weather"}
        <Dropdown
            bind:selected={weatherAttribute}
            choices={weatherAttributeChoices}
            label="Attribute"
        />
    {:else if layer.id === "ndvi"}
        <Dropdown
            bind:selected={ndviAttribute}
            choices={ndviAttributeChoices}
            label="Attribute"
        />
    {/if}
</div>

<div class="flex justify-center mt-5">
    <Legend {colorOptions} />
</div>