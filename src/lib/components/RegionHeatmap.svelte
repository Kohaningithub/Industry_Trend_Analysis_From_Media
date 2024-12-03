<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    
    export let data;
    export let selectedYear;
    export let selectedIndustry;
    
    let width = 900;
    let height = 600;
    let margin = { top: 60, right: 100, bottom: 60, left: 150 };
    
    $: innerWidth = width - margin.left - margin.right;
    $: innerHeight = height - margin.top - margin.bottom;
    
    $: filteredData = data.filter(d => {
      if (selectedYear) {
        if (selectedIndustry === 'All') {
          return d.Year === selectedYear;
        }
        return d.Year === selectedYear && d.Industry === selectedIndustry;
      }
      return false;
    });
  
    $: aggregatedData = d3.rollup(filteredData,
      v => d3.sum(v, d => d.Frequency),
      d => d.Region,
      d => d.Industry
    );
  
    $: regions = Array.from(aggregatedData.keys()).sort();
    $: industries = selectedIndustry === 'All' 
      ? Array.from(new Set(data.map(d => d.Industry))).sort()
      : [selectedIndustry];
  
    $: heatmapData = regions.flatMap(region =>
      industries.map(industry => ({
        region,
        industry,
        value: aggregatedData.get(region)?.get(industry) || 0
      }))
    );
  
    let svg;
  
    $: if (svg && heatmapData) {
      updateVisualization();
    }
  
    function updateVisualization() {
      const svgElement = d3.select(svg);
      svgElement.selectAll("*").remove();
  
      // Create scales
      const xScale = d3.scaleBand()
        .domain(industries)
        .range([0, innerWidth])
        .padding(0.1);
  
      const yScale = d3.scaleBand()
        .domain(regions)
        .range([0, innerHeight])
        .padding(0.1);
  
      const colorScale = d3.scaleSequential()
        .domain([0, d3.max(heatmapData, d => d.value)])
        .interpolator(d3.interpolateBlues);
  
      // Create the main group
      const g = svgElement.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
  
      // Add rectangles for heatmap
      g.selectAll("rect")
        .data(heatmapData)
        .join("rect")
        .attr("x", d => xScale(d.industry))
        .attr("y", d => yScale(d.region))
        .attr("width", xScale.bandwidth())
        .attr("height", yScale.bandwidth())
        .attr("fill", d => colorScale(d.value))
        .attr("rx", 2)
        .attr("ry", 2)
        .append("title")
        .text(d => `${d.region} - ${d.industry}: ${d.value}`);
  
      // Add axes
      const xAxis = d3.axisTop(xScale);
      const yAxis = d3.axisLeft(yScale);
  
      g.append("g")
        .attr("class", "x-axis")
        .call(xAxis)
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");
  
      g.append("g")
        .attr("class", "y-axis")
        .call(yAxis);
  
      // Add title
      svgElement.append("text")
        .attr("x", width / 2)
        .attr("y", margin.top / 2)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .text(`Regional Industry Activity Heatmap (${selectedYear})`);
  
      // Add legend
      const legendWidth = 20;
      const legendHeight = innerHeight;
      const legend = svgElement.append("g")
        .attr("transform", `translate(${width - margin.right + 40},${margin.top})`);
  
      const legendScale = d3.scaleSequential()
        .domain([0, d3.max(heatmapData, d => d.value)])
        .interpolator(d3.interpolateBlues);
  
      const legendAxis = d3.axisRight()
        .scale(d3.scaleLinear()
          .domain([0, d3.max(heatmapData, d => d.value)])
          .range([legendHeight, 0]));
  
      legend.append("g")
        .call(legendAxis);
  
      const legendGradient = legend.append("defs")
        .append("linearGradient")
        .attr("id", "legend-gradient")
        .attr("x1", "0%")
        .attr("x2", "0%")
        .attr("y1", "0%")
        .attr("y2", "100%");
  
      legendGradient.selectAll("stop")
        .data(d3.range(0, 1.1, 0.1))
        .join("stop")
        .attr("offset", d => `${d * 100}%`)
        .attr("stop-color", d => legendScale(d * d3.max(heatmapData, d => d.value)));
  
      legend.append("rect")
        .attr("width", legendWidth)
        .attr("height", legendHeight)
        .style("fill", "url(#legend-gradient)");
    }
  
    onMount(() => {
      updateVisualization();
    });
  </script>
  
  <div class="heatmap-container">
    <svg 
      bind:this={svg}
      {width}
      {height}
    ></svg>
  </div>
  
  <style>
    .heatmap-container {
      margin: 1rem 0;
      overflow-x: auto;
    }
  
    :global(.x-axis text), :global(.y-axis text) {
      font-size: 12px;
    }
  
    :global(.x-axis path), :global(.y-axis path), 
    :global(.x-axis line), :global(.y-axis line) {
      stroke: #ccc;
    }
  </style>