<script lang="ts">
    import Map from "$lib/Map.svelte";
    import Controls from "$lib/Controls.svelte";
    import GeometryCollection from "$lib/GeometryCollection.svelte";
    import Popup from "$lib/Popup.svelte";

    import Selection from "../components/Selection.svelte";
    import Dropdown from "../components/Dropdown.svelte";
    import Slider from "../components/Slider.svelte";
    import Legend from "../components/legend/Legend.svelte";

    import { getColorOptions, getFillColor } from "../components/legend/color";
    import type { Choice } from "../types";

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
        { id: "bulk_density", value: "Bulk Density (10 * kg / m^3)" },
        { id: "clay", value: "Clay Content (%)" },
        { id: "ph", value: "Soil pH (10 * pH in H2O)" },
        { id: "sand", value: "Sand Content (%)" },
        { id: "organic_carbon", value: "Soil Organic Carbon (5 * g / kg)" },
        { id: "water_content", value: "Soil Water Content (%)" },
    ];

    const weatherAttributeChoices: Choice[] = [
        { id: "prcp", value: "Percipitation (mm)" },
        { id: "srad", value: "Solar Radiation (W/m^2)" },
        { id: "swe", value: "Snow Water Equivalent (kg / m^2)" },
        { id: "tmax", value: "Maximum Temperature (C)" },
        { id: "tmin", value: "Minimum Temperature (C)" },
        { id: "vp", value: "Water Vapor Pressure (Pa)" },
    ];

    const ndviAttributeChoices: Choice[] = [{ id: "ndvi", value: "NDVI" }];

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

    let fillOpacity = 0.8;

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
        return "bulk_density_0";
    }

    function getMinMax(column: string) {
        if (column.startsWith("bulk_density")) {
            return [50, 200];
        }
        if (column.startsWith("clay")) {
            return [0, 50];
        }
        if (column.startsWith("ph")) {
            return [40, 100];
        }
        if (column.startsWith("sand")) {
            return [0, 100];
        }
        if (column.startsWith("organic_carbon")) {
            return [0, 60];
        }
        if (column.startsWith("water_content")) {
            return [0, 60];
        }
        if (column.startsWith("prcp")) {
            return [0, 10];
        }
        if (column.startsWith("srad")) {
            return [200, 600];
        }
        if (column.startsWith("swe")) {
            return [0, 1500];
        }
        if (column.startsWith("tmax")) {
            return [-20, 40];
        }
        if (column.startsWith("tmin")) {
            return [-20, 40];
        }
        if (column.startsWith("vp")) {
            return [200, 1400];
        }
        if (column.startsWith("ndvi")) {
            return [0, 0.5];
        }
    }

    $: column = getColumn(
        layer,
        soilAttribute,
        weatherAttribute,
        ndviAttribute,
        depth
    );

    $: [min, max] = getMinMax(column);
    $: colorOptions = getColorOptions(min, max);
    $: fillColor = getFillColor(column, colorOptions);

    const getHTML = (e: any) => {
        let { properties } = e.features[0];
        let value = Math.round(properties[column] * 100) / 100;

        return `<p><b>${value}</b></p>`;
    };
</script>

<Legend {colorOptions} {fillOpacity} />

<Map lng={-120.0} lat={37.5} zoom={4}>
    <Controls />
    <GeometryCollection
        sourceUrl="mapbox://danny-darko.d4v2kznn"
        sourceLayer="california_25000-dh558w"
        sourceName="gridSource_25000"
        layerName="gridLayer_25000"
        bind:fillColor
        {fillOpacity}
        minZoom={0}
        maxZoom={6}
    />
    <Popup layerName="gridLayer_25000" {getHTML} />
    <GeometryCollection
        sourceUrl="mapbox://danny-darko.945a4o5j"
        sourceLayer="california_10000-4u0y3s"
        sourceName="gridSource_10000"
        layerName="gridLayer_10000"
        bind:fillColor
        {fillOpacity}
        minZoom={6}
        maxZoom={8}
    />
    <Popup layerName="gridLayer_10000" {getHTML} />
    <GeometryCollection
        sourceUrl="mapbox://danny-darko.96hf0e0o"
        sourceLayer="california_5000-2ku4fl"
        sourceName="gridSource_5000"
        layerName="gridLayer_5000"
        bind:fillColor
        {fillOpacity}
        minZoom={8}
        maxZoom={24}
    />
    <Popup layerName="gridLayer_5000" {getHTML} />
</Map>

<div class="w-auto border-t-[0.1rem] border-black border-solid">
    <Selection bind:selected={layer} choices={layerChoices} />
    {#if layer.id === "soil"}
        <Dropdown
            bind:selected={soilAttribute}
            choices={soilAttributeChoices}
        />
        <Slider bind:selected={depth} choices={depthChoices} />
    {:else if layer.id === "weather"}
        <Dropdown
            bind:selected={weatherAttribute}
            choices={weatherAttributeChoices}
        />
    {:else if layer.id === "ndvi"}
        <Dropdown
            bind:selected={ndviAttribute}
            choices={ndviAttributeChoices}
        />
    {/if}
</div>
