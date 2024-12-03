<script>
    import * as d3 from 'd3';
    export let data;

    const width = 800;
    const height = 400;
    const margin = { top: 20, right: 150, bottom: 40, left: 200 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Process data to compare before and after March 2019
    $: processedData = d3.groups(data, d => d.sector)
        .map(([sector, values]) => {
            const before = values
                .filter(d => (d.year < 2019 || (d.year === 2019 && d.month <= 3)))
                .reduce((sum, d) => sum + d.frequency, 0);
                
            const after = values
                .filter(d => (d.year > 2019 || (d.year === 2019 && d.month > 3)))
                .reduce((sum, d) => sum + d.frequency, 0);

            return {
                sector,
                before,
                after,
                difference: after - before
            };
        })
        .sort((a, b) => b.difference - a.difference); // Sort by biggest change

    // Scales
    $: yScale = d3.scaleBand()
        .domain(processedData.map(d => d.sector))
        .range([0, innerHeight])
        .padding(0.2);

    $: xScale = d3.scaleLinear()
        .domain(d3.extent([
            ...processedData.map(d => d.before),
            ...processedData.map(d => d.after)
        ]))
        .range([0, innerWidth]);
</script>

<div class="chart-container">
    <svg {width} {height}>
        <g transform="translate({margin.left},{margin.top})">
            <!-- Sector names -->
            {#each processedData as item}
                <text
                    x={-10}
                    y={yScale(item.sector) + yScale.bandwidth() / 2}
                    text-anchor="end"
                    dominant-baseline="middle"
                    class="sector-label"
                >
                    {item.sector}
                </text>
            {/each}

            <!-- Y-axis (sectors) -->
            <g class="axis">
                {#if yScale}
                    {@const yAxis = d3.axisLeft(yScale)}
                    {@const yAxisGroup = d3.select(null)}
                    {@const _ = yAxisGroup?.call(yAxis)}
                {/if}
            </g>

            <!-- X-axis (frequency) -->
            <g transform="translate(0,{innerHeight})" class="axis">
                {#if xScale}
                    {@const xAxis = d3.axisBottom(xScale)}
                    {@const xAxisGroup = d3.select(null)}
                    {@const _ = xAxisGroup?.call(xAxis)}
                {/if}
            </g>

            <!-- Bars -->
            {#each processedData as item}
                <!-- Before March 2019 bars -->
                <rect
                    x={xScale(Math.min(0, item.before))}
                    y={yScale(item.sector)}
                    width={Math.abs(xScale(item.before) - xScale(0))}
                    height={yScale.bandwidth()}
                    fill="#69b3a2"
                    opacity="0.8"
                >
                    <title>{item.sector}: {item.before.toFixed(1)}</title>
                </rect>
                
                <!-- After March 2019 bars -->
                <rect
                    x={xScale(Math.min(0, item.after))}
                    y={yScale(item.sector) + yScale.bandwidth() / 2}
                    width={Math.abs(xScale(item.after) - xScale(0))}
                    height={yScale.bandwidth() / 2}
                    fill="#404080"
                    opacity="0.8"
                >
                    <title>{item.sector}: {item.after.toFixed(1)}</title>
                </rect>
            {/each}

            <!-- Legend -->
            <g transform="translate({innerWidth + 10}, 0)">
                <rect x="0" y="0" width="20" height="10" fill="#69b3a2" />
                <text x="25" y="9">Before March 2019</text>
                <rect x="0" y="20" width="20" height="10" fill="#404080" />
                <text x="25" y="29">After March 2019</text>
            </g>
        </g>
    </svg>
</div>

<style>
    .chart-container {
        width: 100%;
        margin: 20px 0;
    }

    .axis path,
    .axis line {
        stroke: #ccc;
    }

    .axis text {
        font-size: 12px;
    }

    text {
        fill: #666;
        font-size: 12px;
    }

    rect:hover {
        opacity: 1;
    }

    .sector-label {
        font-size: 12px;
        fill: #333;
    }

    /* Make text unselectable for better UX */
    text {
        user-select: none;
    }
</style>