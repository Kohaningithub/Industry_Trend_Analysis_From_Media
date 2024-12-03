<script>
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    export let data;

    let svg;
    let brush;
    let selectedSectors = new Set();
    let hoveredSector = null;

    $: sectors = [...new Set(data.map(d => d.sector))];
    $: if (sectors) {
        selectedSectors = new Set(['Information Technology']);
    }

    $: if (data && svg) {
        updateChart();
    }

    function brushed(event) {
        if (!event.selection) return;
        
        const [x0, x1] = event.selection.map(xScale.invert);
    
        // Update domain and clear brush
        xScale.domain([x0, x1]);
        d3.select(svg).select('.brush').call(brush.move, null);
        
            updateChart();
        }

    function updateChart() {
        const margin = { top: 20, right: 10, bottom: 80, left: 60 };
        const width = 800 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        // Clear previous content
        d3.select(svg).selectAll('*').remove();

        // Process data
        const processedData = d3.groups(data, d => d.sector)
            .map(([sector, values]) => ({
                sector,
                values: values.map(d => ({
                    date: new Date(d.year, d.month - 1),
                    value: d.frequency
                })).sort((a, b) => a.date - b.date)
            }));

        // Create scales
        const xScale = d3.scaleTime()
            .domain(d3.extent(data, d => new Date(d.year, d.month - 1)))
            .range([0, width]);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.frequency)* 0.9])
            .range([height, 0])
            .nice();

        const colorScale = d3.scaleOrdinal(d3.schemeCategory10)
            .domain(sectors);

        // Create the SVG group with margins
        const g = d3.select(svg)
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Add lines
        const line = d3.line()
            .x(d => xScale(d.date))
            .y(d => yScale(d.value));

        processedData.forEach(({ sector, values }) => {
            if (selectedSectors.has(sector)) {
                g.append('path')
                    .datum(values)
                    .attr('class', 'line')
                    .attr('data-sector', sector)
                    .attr('fill', 'none')
                    .attr('stroke', colorScale(sector))
                    .attr('stroke-width', 2)
                    .attr('d', line);
            }
        });

        // Add X axis
        g.append('g')
            .attr('transform', `translate(0,${height})`)
            .attr('class', 'x-axis')
            .call(d3.axisBottom(xScale)
                .ticks(d3.timeMonth.every(6))
                .tickFormat(d3.timeFormat("%b %Y")))
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em')
            .attr('transform', 'rotate(-45)');

        // Add Y axis
        g.append('g')
            .attr('class', 'y-axis')
            .call(d3.axisLeft(yScale));

        // Add brush
        brush = d3.brushX()
            .extent([[0, 0], [width, height]])
            .on('end', brushed);

        g.append('g')
            .attr('class', 'brush')
            .call(brush);

        function brushed(event) {
            if (!event.selection) return;
            
            const [x0, x1] = event.selection.map(xScale.invert);
            
            // Update the lines based on the brush selection
            xScale.domain([x0, x1]);
            
            // Update x-axis
            g.select('.x-axis')
                .transition()
                .duration(750)
                .call(d3.axisBottom(xScale)
                    .ticks(d3.timeMonth.every(6))
                    .tickFormat(d3.timeFormat("%b %Y")));

            // Update lines
            g.selectAll('.line')
                .transition()
                .duration(750)
                .attr('d', function() {
                    const sector = this.getAttribute('data-sector');
                    const sectorData = processedData.find(d => d.sector === sector);
                    return line(sectorData.values);
                });
        }

        // Add axis labels
        g.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', 0 - margin.left)
            .attr('x', 0 - (height / 2))
            .attr('dy', '1em')
            .attr('class', 'axis-label')
            .style('text-anchor', 'middle')
            .text('Frequency');

        g.append('text')
            .attr('x', width / 2)
            .attr('y', height + margin.bottom - 5)
            .attr('class', 'axis-label')
            .style('text-anchor', 'middle')
            .text('Time');
    }

    function toggleSector(sector) {
        if (selectedSectors.has(sector)) {
            selectedSectors.delete(sector);
        } else {
            selectedSectors.add(sector);
        }
        selectedSectors = selectedSectors;
        updateChart();
    }
</script>

<div class="chart-container">
        <svg bind:this={svg}></svg>

        <div class="legend">
            {#each sectors as sector}
                <div 
                    class="legend-item"
                    on:mouseover={() => hoveredSector = sector}
                    on:mouseout={() => hoveredSector = null}
                >
                    <label>
                        <input
                            type="checkbox"
                            checked={selectedSectors.has(sector)}
                            on:change={() => toggleSector(sector)}
                        />
                        <span class="color-dot" style="background-color: {d3.schemeCategory10[sectors.indexOf(sector)]}"></span>
                        <span class="sector-name">{sector}</span>
                    </label>
                </div>
            {/each}
        </div>
</div>

<style>
    .chart-container {
        width: 100%;
        display: flex;
        align-items: flex-start;
        gap: 20px;
    }

    .grid-background {
        fill: #ffffff;
    }

    .legend {
        padding: 10px;
        background: #f5f5f5;
        border-radius: 4px;
        max-height: 400px;
        overflow-y: auto;
    }

    .legend-item {
        margin: 8px 0;
    }

    .legend-item label {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
    }

    .color-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
    }

    .sector-name {
        font-size: 14px;
    }

    .line {
        stroke-width: 2;
        transition: all 0.2s ease;
    }

    .line.highlighted {
        stroke-width: 4;
        opacity: 1;
        z-index: 2;
    }

    .line.dimmed {
        opacity: 0.1;
    }

    .axis-label {
        fill: #666;
        font-size: 12px;
    }

    :global(.x-axis path),
    :global(.y-axis path) {
        stroke: #666;
    }

    :global(.x-axis line),
    :global(.y-axis line) {
        stroke: #ddd;
    }

    :global(.x-axis text),
    :global(.y-axis text) {
        fill: #666;
        font-size: 12px;
    }

    :global(.y-axis .tick line) {
        stroke: #e0e0e0;
        stroke-dasharray: 2,2;
    }

    input[type="checkbox"] {
        cursor: pointer;
    }

    :global(.brush .selection) {
        fill: rgba(105, 179, 162, 0.2);
        stroke: #69b3a2;
        stroke-width: 1px;
    }

    :global(.brush .handle) {
        fill: #69b3a2;
    }

    :global(.brush .overlay) {
        cursor: crosshair;
    }

    /* Add transition styles for smoother updates */
    .line {
        stroke-width: 2;
        transition: all 0.2s ease;
    }

    :global(.line) {
        transition: d 0.75s ease;
    }
</style>