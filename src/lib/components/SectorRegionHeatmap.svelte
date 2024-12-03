<script>
    import * as d3 from 'd3';
    export let data;

    let width = 800;
    let height = 500;
    let margin = { top: 60, right: 40, bottom: 100, left: 120 };

    $: innerWidth = width - margin.left - margin.right;
    $: innerHeight = height - margin.top - margin.bottom;

    $: processedData = (() => {
        // Group and count data
        const counts = d3.rollup(data,
            v => v.length,
            d => d.sector,
            d => d.region
        );

        // Convert to array format
        const result = [];
        counts.forEach((regionCounts, sector) => {
            regionCounts.forEach((count, region) => {
                result.push({ sector, region, count });
            });
        });
        return result;
    })();

    $: sectors = [...new Set(processedData.map(d => d.sector))];
    $: regions = [...new Set(processedData.map(d => d.region))];
    
    $: colorScale = d3.scaleSequential()
        .domain([0, d3.max(processedData, d => d.count)])
        .interpolator(d3.interpolateYlOrRd);
</script>

<div class="chart-container">
    <svg {width} {height}>
        <g transform="translate({margin.left},{margin.top})">
            <!-- Y-axis (Sectors) -->
            {#each sectors as sector, i}
                <text
                    x="-10"
                    y={i * (innerHeight / sectors.length) + (innerHeight / sectors.length) / 2}
                    text-anchor="end"
                    dominant-baseline="middle"
                >
                    {sector}
                </text>
            {/each}

            <!-- X-axis (Regions) -->
            {#each regions as region, i}
                <text
                    x={i * (innerWidth / regions.length) + (innerWidth / regions.length) / 2}
                    y={innerHeight + 20}
                    text-anchor="end"
                    transform="rotate(-45, {i * (innerWidth / regions.length) + (innerWidth / regions.length) / 2}, {innerHeight + 20})"
                >
                    {region}
                </text>
            {/each}

            <!-- Heatmap cells -->
            {#each processedData as d}
                {@const sectorIndex = sectors.indexOf(d.sector)}
                {@const regionIndex = regions.indexOf(d.region)}
                <rect
                    x={regionIndex * (innerWidth / regions.length)}
                    y={sectorIndex * (innerHeight / sectors.length)}
                    width={innerWidth / regions.length}
                    height={innerHeight / sectors.length}
                    fill={colorScale(d.count)}
                    stroke="white"
                    stroke-width="1"
                >
                    <title>{d.sector} - {d.region}: {d.count} mentions</title>
                </rect>
            {/each}
        </g>
    </svg>
</div>

<style>
    .chart-container {
        margin: 2rem auto;
    }
    text {
        font-size: 12px;
    }
</style>