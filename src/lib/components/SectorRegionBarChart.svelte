<script>
    import * as d3 from 'd3';
    export let data;
    export let selectedYear;
    export let selectedSector;

    let width = 1000;
    let height = 400;
    let margin = { top: 30, right: 180, bottom: 40, left: 180 };

    $: innerWidth = width - margin.left - margin.right;
    $: innerHeight = height - margin.top - margin.bottom;

    $: processedData = (() => {
        // Filter out "其他" before processing
        const filteredData = data.filter(d => d.region !== "其他" && d.region !== "Others");

        // Group and sum by sector and region
        const grouped = d3.rollup(filteredData,
            v => d3.sum(v, d => d.count),
            d => d.sector,
            d => d.region
        );

        // Get top region for each sector
        return Array.from(grouped)
            .map(([sector, regions]) => {
                const topRegion = Array.from(regions)
                    .sort((a, b) => b[1] - a[1])[0];
                return {
                    sector,
                    region: topRegion[0],
                    count: topRegion[1]
                };
            })
            .sort((a, b) => b.count - a.count); // Sort by count
    })();

    $: yScale = d3.scaleBand()
        .domain(processedData.map(d => d.sector))
        .range([0, innerHeight])
        .padding(0.3);

    $: xScale = d3.scaleLinear()
        .domain([0, d3.max(processedData, d => d.count)])
        .range([0, innerWidth])
        .nice();

    $: colorScale = d3.scaleOrdinal()
        .domain(processedData.map(d => d.region))
        .range(d3.schemeCategory10);
</script>

<div class="chart-container">
    <h3>Leading Regions by Sector</h3>
    <svg {width} {height}>
        <g transform="translate({margin.left},{margin.top})">
            <!-- Y-axis (Sectors) -->
            {#each processedData as d}
                <text
                    x="-10"
                    y={yScale(d.sector) + yScale.bandwidth() / 2}
                    text-anchor="end"
                    dominant-baseline="middle"
                    font-size="12px"
                >
                    {d.sector}
                </text>
            {/each}

            <!-- X-axis -->
            <g transform="translate(0,{innerHeight})">
                <line x1={0} x2={innerWidth} y1={0} y2={0} stroke="#ccc" />
                {#each xScale.ticks(5) as tick}
                    <g transform="translate({xScale(tick)},0)">
                        <line y1={0} y2={5} stroke="#ccc" />
                        <text
                            y={20}
                            text-anchor="middle"
                            font-size="12px"
                        >
                            {tick}
                        </text>
                    </g>
                {/each}
                <text
                    x={innerWidth / 2}
                    y={35}
                    text-anchor="middle"
                    font-size="12px"
                >
                    Number of Mentions
                </text>
            </g>

            <!-- Grid lines -->
            {#each xScale.ticks(5) as tick}
                <line
                    x1={xScale(tick)}
                    x2={xScale(tick)}
                    y1={0}
                    y2={innerHeight}
                    stroke="#eee"
                    stroke-dasharray="2,2"
                />
            {/each}

            <!-- Bars -->
            {#each processedData as d}
                <g transform="translate(0,{yScale(d.sector)})">
                    <rect
                        x={0}
                        y={0}
                        width={xScale(d.count)}
                        height={yScale.bandwidth()}
                        fill={colorScale(d.region)}
                        opacity={0.8}
                    >
                        <title>{d.sector} - {d.region}: {d.count}</title>
                    </rect>
                    <!-- Region label -->
                    <text
                        x={xScale(d.count) + 5}
                        y={yScale.bandwidth() / 2}
                        dominant-baseline="middle"
                        font-size="12px"
                        fill="#666"
                    >
                        {d.region}
                    </text>
                </g>
            {/each}
        </g>
    </svg>
</div>

<style>
    .chart-container {
        margin: 2rem auto;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    h3 {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 1rem;
    }

    svg {
        width: 100%;
        height: auto;
        max-width: 1000px;
        margin: 0 auto;
        display: block;
    }

    .note {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background: #f8f9fa;
        border-left: 3px solid #4a90e2;
        border-radius: 4px;
    }
</style>