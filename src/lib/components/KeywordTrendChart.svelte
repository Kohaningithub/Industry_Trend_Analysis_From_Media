<script>
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
  
    export let data = [];
    export let selectedKeyword = '';
  
    let svg;
    let width = 600;
    let height = 400;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
  
    $: innerWidth = width - margin.left - margin.right;
    $: innerHeight = height - margin.top - margin.bottom;
  
    $: xScale = d3.scaleTime()
      .domain(d3.extent(data, d => new Date(d.year, 0, 1)))
      .range([0, innerWidth]);
  
    $: yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.count)])
      .range([innerHeight, 0])
      .nice();
  
    $: line = d3.line()
      .x(d => xScale(new Date(d.year, 0, 1)))
      .y(d => yScale(d.count));
  
    $: area = d3.area()
      .x(d => xScale(new Date(d.year, 0, 1)))
      .y0(innerHeight)
      .y1(d => yScale(d.count));
  
    function updateChart() {
      if (!svg || !data.length) return;
  
      const chart = d3.select(svg);
  
      // 清除现有内容
      chart.selectAll('*').remove();
  
      // 创建主要的绘图区域
      const g = chart.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
  
      // 添加渐变区域
      g.append('path')
        .datum(data)
        .attr('class', 'area')
        .attr('d', area)
        .attr('fill', 'url(#area-gradient)');
  
      // 添加趋势线
      g.append('path')
        .datum(data)
        .attr('class', 'line')
        .attr('d', line)
        .attr('fill', 'none')
        .attr('stroke', '#2196f3')
        .attr('stroke-width', 2);
  
      // 添加数据点
      g.selectAll('.dot')
        .data(data)
        .enter()
        .append('circle')
        .attr('class', 'dot')
        .attr('cx', d => xScale(new Date(d.year, 0, 1)))
        .attr('cy', d => yScale(d.count))
        .attr('r', 4)
        .attr('fill', '#2196f3');
  
      // 添加 X 轴
      g.append('g')
        .attr('transform', `translate(0,${innerHeight})`)
        .call(d3.axisBottom(xScale)
          .ticks(d3.timeYear)
          .tickFormat(d3.timeFormat('%Y')));
  
      // 添加 Y 轴
      g.append('g')
        .call(d3.axisLeft(yScale));
  
      // 添加标题
      g.append('text')
        .attr('x', innerWidth / 2)
        .attr('y', -margin.top / 2)
        .attr('text-anchor', 'middle')
        .attr('class', 'chart-title')
        .text(`${selectedKeyword} 提及频率趋势`);
    }
  
    $: if (data && svg) {
      updateChart();
    }
  </script>
  
  <div class="chart-container">
    <svg
      bind:this={svg}
      {width}
      {height}
    >
      <defs>
        <linearGradient id="area-gradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#2196f3" stop-opacity="0.4"/>
          <stop offset="100%" stop-color="#2196f3" stop-opacity="0.1"/>
        </linearGradient>
      </defs>
    </svg>
  </div>
  
  <style>
    .chart-container {
      width: 100%;
      max-width: 800px;
      margin: 2rem auto;
      background: white;
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  
    svg {
      width: 100%;
      height: auto;
    }
  
    :global(.chart-title) {
      font-size: 16px;
      font-weight: bold;
    }
  
    :global(.line) {
      transition: all 0.3s ease;
    }
  
    :global(.dot) {
      transition: all 0.3s ease;
    }
  
    :global(.dot:hover) {
      r: 6;
      fill: #1976d2;
    }
  
    :global(.area) {
      transition: all 0.3s ease;
    }
  </style>