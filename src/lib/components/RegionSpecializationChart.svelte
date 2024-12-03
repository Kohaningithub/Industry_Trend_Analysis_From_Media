<script>
    import * as d3 from 'd3';
    export let data;

    let width = 800;
    let height = 400;
    let margin = { top: 40, right: 100, bottom: 60, left: 100 };

    $: innerWidth = width - margin.left - margin.right;
    $: innerHeight = height - margin.top - margin.bottom;

    $: yScale = d3.scaleBand()
        .domain(data.map(d => d.region))
        .range([0, innerHeight])
        .padding(0.2);

    $: xScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.specialization)])
        .range([0, innerWidth]);

    $: colorScale = d3.scaleOrdinal()
        .domain(data.map(d => d.sector))
        .range(d3.schemeCategory10);
</script>

<div class="chart">
    <svg {width} {height}>
        <g transform="translate({margin.left}, {margin.top})">
            <!-- Axes -->
            <!-- Bars -->
            {#each data as d}
                <rect
                    x={0}
                    y={yScale(d.region)}
                    width={xScale(d.specialization)}
                    height={yScale.bandwidth()}
                    fill={colorScale(d.sector)}
                    opacity={0.8}
                >
                    <title>
                        {d.region}: {d.sector}
                        Specialization: {d.specialization.toFixed(1)}x
                        Share: {d.share.toFixed(1)}%
                    </title>
                </rect>
            {/each}
        </g>
    </svg>
</div>

<style>
    .chart {
        margin: 2rem 0;
    }
</style>