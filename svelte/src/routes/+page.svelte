<script lang="ts">
    import MapBox from "../components/MapBox.svelte";
    import Selection from "../components/Selection.svelte";
    import Dropdown from "../components/Dropdown.svelte";
    import Slider from "../components/Slider.svelte";
    import Legend from "../components/legend/Legend.svelte";

    import { getColorOptions } from "../components/legend/color";
    import type { Choice } from "../types";
    import countyData from "$lib/data/california.json";

    const layerChoices: Choice[] = [
        { id: "soil", value: "Soil", icon: "mdi:shovel" },
        { id: "weather", value: "Weather", icon: "bi:cloud-rain-fill" },
        {
            id: "ndvi",
            value: "Vegetation",
            icon: "material-symbols:potted-plant-rounded",
        },
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

    $: values = countyData.features.map((feature) => {
        let properties: any = feature.properties;
        return properties[column];
    });
    $: colorOptions = getColorOptions(values);
</script>

<Legend {colorOptions} />
<MapBox {column} {colorOptions} {countyData} />

<Selection bind:selected={layer} choices={layerChoices} />
{#if layer.id === "soil"}
    <Dropdown bind:selected={soilAttribute} choices={soilAttributeChoices} />
    <Slider bind:selected={depth} choices={depthChoices} />
{:else if layer.id === "weather"}
    <Dropdown
        bind:selected={weatherAttribute}
        choices={weatherAttributeChoices}
    />
{:else if layer.id === "ndvi"}
    <Dropdown bind:selected={ndviAttribute} choices={ndviAttributeChoices} />
{/if}
