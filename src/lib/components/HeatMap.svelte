<script>
    import * as d3 from 'd3';
    export let data;

    const width = 1000;
    const height = 500;
    const margin = { top: 40, right: 160, bottom: 60, left: 160 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    const legendHeight = 200;
    const legendWidth = 20;

    // Process data for heatmap format
    $: processedData = d3.groups(data, d => d.year)
        .flatMap(([year, yearData]) =>
            d3.groups(yearData, d => d.month)
                .flatMap(([month, monthData]) =>
                    monthData.map(d => ({
                        sector: d.sector,
                        year: d.year,
                        month: d.month,
                        frequency: d.frequency
                    }))
                )
        );

    // Get unique sectors and time points
    $: sectors = [...new Set(data.map(d => d.sector))];
    $: timePoints = [...new Set(data.map(d => `${d.year}-${d.month}`))].sort();

    // Scales
    $: yScale = d3.scaleBand()
        .domain(sectors)
        .range([0, innerHeight])
        .padding(0.1);

    $: xScale = d3.scaleBand()
        .domain(timePoints)
        .range([0, innerWidth])
        .padding(0.1);

    // Color scale for frequency intensity
    $: colorScale = d3.scaleSequential(d3.interpolateBlues)
        .domain([0, d3.max(data, d => d.frequency)]);

    // Format date for tooltip
    const formatDate = (year, month) => {
        const date = new Date(year, month - 1);
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
    };

    // Format date for axis
    const formatMonth = (year, month) => {
        const date = new Date(year, month - 1);
        return date.toLocaleDateString('en-US', { month: 'short' });
    };

    // Add axis labels
    const xAxisLabel = "Time (2015-2023)";
    const yAxisLabel = "Technological Sectors";

    // Modify the X-axis formatting
    const formatXAxisTick = (timeKey) => {
        const [year, month] = timeKey.split('-');
        if (month === '1') {
            return year;
        } else if (month === '7') {
            return formatMonth(parseInt(year), parseInt(month));
        }
        return '';
    };
</script>

<div class="chart-container">
    <svg {width} {height}>
        <g transform="translate({margin.left},{margin.top})">
            <!-- Y-axis with sector names -->
            <g class="y-axis">
                {#each sectors as sector}
                    <text
                        x={-10}
                        y={yScale(sector) + yScale.bandwidth() / 2}
                        text-anchor="end"
                        dominant-baseline="middle"
                        class="sector-label"
                    >
                        {sector}
                    </text>
                {/each}
            </g>

            <!-- X-axis with time labels -->
            <g transform="translate(0,{innerHeight})" class="x-axis">
                {#each timePoints as timePoint}
                    <text
                        x={xScale(timePoint) + xScale.bandwidth() / 2}
                        y={25}
                        text-anchor="middle"
                        transform="rotate(-45, {xScale(timePoint) + xScale.bandwidth() / 2}, 25)"
                        class="time-label"
                    >
                        {formatXAxisTick(timePoint)}
                    </text>
                {/each}
            </g>

            <!-- Heat map cells -->
            {#each processedData as d}
                {@const timeKey = `${d.year}-${d.month}`}
                <rect
                    x={xScale(timeKey)}
                    y={yScale(d.sector)}
                    width={xScale.bandwidth()}
                    height={yScale.bandwidth()}
                    fill={colorScale(d.frequency)}
                    opacity="0.8"
                    class="heatmap-cell"
                >
                    <title>
                        {d.sector}
                        {formatDate(d.year, d.month)}
                        Frequency: {d.frequency}
                    </title>
                </rect>
            {/each}

            <!-- Legend -->
            <g transform="translate({innerWidth + 20}, 0)" class="legend">
                {#each d3.range(0, legendHeight) as i}
                    <rect
                        x="0"
                        y={i}
                        width={legendWidth}
                        height="1"
                        fill={colorScale(d3.max(data, d => d.frequency) * (1 - i / legendHeight))}
                    />
                {/each}
                <text x={legendWidth + 5} y="-5" class="legend-label">Frequency</text>
                <text x={legendWidth + 5} y="15">High</text>
                <text x={legendWidth + 5} y={legendHeight}>Low</text>
            </g>
        </g>
    </svg>
</div>

<style>
    .chart-container {
        background: transparent;
        width: 100%;
        margin: 20px;
        background: white;
        padding: 20px;
        border-radius: 8px;
    }

    .sector-label {
        font-size: 12px;
        fill: #333;
    }

    .time-label {
        font-size: 10px;
        fill: #666;
    }

    .heatmap-cell:hover {
        opacity: 1;
        stroke: #333;
        stroke-width: 1px;
        cursor: pointer;
    }

    .legend-label {
        font-size: 12px;
        font-weight: bold;
        fill: #333;
    }

    /* Make gridlines lighter */
    .y-axis line {
        stroke: #eee;
        stroke-dasharray: 2,2;
    }

    /* Hide axis lines but keep ticks */
    .y-axis path,
    .x-axis path {
        display: none;
    }
</style>