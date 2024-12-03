<script>
    import * as d3 from 'd3';
    export let regionalData;

    let selectedRegion = 'All';
    let selectedSector = 'All';

    // 预定义行业顺序和颜色
    const sectorOrder = [
        'Agricultural Machinery',
        'Biopharmaceuticals',
        'Information Technology',
        'New Energy Vehicles',
        'New Materials',
        'Ocean Engineering',
        'Rail Transit',
        'Robotics'
    ];

    const sectorColors = {
        'Information Technology': '#2ca02c',    // 绿色
        'New Energy Vehicles': '#d62728',       // 红色
        'New Materials': '#9467bd',             // 紫色
        'Rail Transit': '#e377c2',              // 粉色
        'Robotics': '#7f7f7f',                  // 灰色
        'Agricultural Machinery': '#1f77b4',    // 蓝色
        'Biopharmaceuticals': '#ff7f0e',       // 橙色
        'Ocean Engineering': '#8c564b'          // 棕色
    };

    // 获取所有可用的地区和行业，并按预定义顺序排序
    $: regions = [...new Set(regionalData.map(d => d.region))]
        .filter(r => r !== 'Others' && r !== '其他')
        .sort();
    
    // 确保sectors按预定义顺序排序
    $: sectors = sectorOrder.filter(sector => 
        new Set(regionalData.map(d => d.sector)).has(sector)
    );

    // 获取特定地区的行业数据
    $: availableSectors = selectedRegion === 'All' 
        ? sectors 
        : [...new Set(
            regionalData
                .filter(d => d.region === selectedRegion && d.count > 0)
                .map(d => d.sector)
          )].sort((a, b) => sectorOrder.indexOf(a) - sectorOrder.indexOf(b));

    // 修改数据处理逻辑
    $: timeSeriesData = d3.rollup(
        regionalData.filter(d => 
            (selectedRegion === 'All' || d.region === selectedRegion) &&
            (selectedSector === 'All' || d.sector === selectedSector) &&
            d.region !== 'Others' && 
            d.region !== '其他'
        ),
        v => d3.sum(v, d => d.count),
        d => d.year,
        // 当选择特定地区时，按sector分组；选择All时也按sector分组
        d => selectedRegion === 'All' ? d.sector : d.sector
    );

    // 转换数据为图表格式
    $: chartData = Array.from(timeSeriesData, ([year, data]) => ({
        year,
        ...Object.fromEntries(data)
    })).sort((a, b) => a.year - b.year);

    // 获取当前要显示的维度列表
    $: displayItems = selectedRegion === 'All' ? sectors : availableSectors;

    // 设置图表尺寸
    let width = 800;
    let height = 400;
    let margin = { top: 20, right: 180, bottom: 30, left: 60 };

    $: innerWidth = width - margin.left - margin.right;
    $: innerHeight = height - margin.top - margin.bottom;

    // 比例尺
    $: xScale = d3.scaleLinear()
        .domain(d3.extent(chartData, d => d.year))
        .range([0, innerWidth]);

    $: yScale = d3.scaleLinear()
        .domain([0, d3.max(chartData, d => {
            return d3.max(displayItems, item => d[item] || 0);
        })])
        .range([innerHeight, 0]);

    // 线条生成器
    $: line = d3.line()
        .x(d => xScale(d.year))
        .y(d => yScale(d.value))
        .curve(d3.curveMonotoneX);

    // 修改颜色比例尺
    $: colorScale = (item) => sectorColors[item] || '#999';
</script>

<div class="temporal-analysis">
    <div class="controls">
        <div class="select-container">
            <label for="region">Region:</label>
            <select id="region" bind:value={selectedRegion}>
                <option value="All">All Regions</option>
                {#each regions as region}
                    <option value={region}>{region}</option>
                {/each}
            </select>
        </div>
        <div class="select-container">
            <label for="sector">Sector:</label>
            <select id="sector" bind:value={selectedSector}>
                <option value="All">All Sectors</option>
                {#each sectors as sector}
                    <option value={sector}>{sector}</option>
                {/each}
            </select>
        </div>
    </div>

    <div class="chart">
        <svg {width} {height}>
            <g transform="translate({margin.left},{margin.top})">
                <!-- X轴 -->
                <g transform="translate(0,{innerHeight})">
                    {#each xScale.ticks() as tick}
                        <g transform="translate({xScale(tick)},0)">
                            <line y2="6" stroke="currentColor" />
                            <text y="9" dy="0.71em" text-anchor="middle">
                                {tick}
                            </text>
                        </g>
                    {/each}
                    <text
                        x={innerWidth/2}
                        y="30"
                        text-anchor="middle"
                    >
                        Year
                    </text>
                </g>

                <!-- Y轴 -->
                <g>
                    {#each yScale.ticks() as tick}
                        <g transform="translate(0,{yScale(tick)})">
                            <line x2={innerWidth} stroke="#ddd" />
                            <text x="-9" dy="0.32em" text-anchor="end">
                                {tick}
                            </text>
                        </g>
                    {/each}
                    <text
                        transform="rotate(-90)"
                        x={-innerHeight/2}
                        y="-40"
                        text-anchor="middle"
                    >
                        Number of Mentions
                    </text>
                </g>

                <!-- 数据线 -->
                {#each displayItems as item}
                    {@const itemData = chartData.map(d => ({
                        year: d.year,
                        value: d[item] || 0
                    }))}
                    <path
                        d={line(itemData)}
                        stroke={colorScale(item)}
                        fill="none"
                        stroke-width="2"
                        opacity="0.8"
                    />
                {/each}

                <!-- 图例 -->
                <g transform="translate({innerWidth + 10}, 0)">
                    {#each displayItems as item, i}
                        <g transform="translate(0,{i * 20})">
                            <line
                                x1="0"
                                x2="20"
                                stroke={sectorColors[item]}
                                stroke-width="2"
                            />
                            <text 
                                x="25" 
                                dy="0.32em" 
                                font-size="12px"
                                fill="#333"
                            >
                                {item}
                            </text>
                        </g>
                    {/each}
                </g>
            </g>
        </svg>
    </div>
</div>

<style>
    .temporal-analysis {
        padding: 1rem;
    }

    .controls {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        justify-content: center;
    }

    .select-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    select {
        padding: 0.5rem;
        border-radius: 4px;
        border: 1px solid #ddd;
        min-width: 150px;
    }

    .chart {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    text {
        font-size: 12px;
        fill: #666;
    }
</style>