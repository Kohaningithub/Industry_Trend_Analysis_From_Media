<script>
    import * as d3 from 'd3';
    import SectorRegionBarChart from './SectorRegionBarChart.svelte';
    import RegionSpecializationChart from './RegionSpecializationChart.svelte';
  
    export let regionalData;
    export let selectedYear;
    export let selectedSector;

    let isTimeRange = false;
    let yearRange = [2021, 2023]; // 默认范围
    let minYear, maxYear;

    // 在数据加载后设置年份范围
    $: {
        if (regionalData.length > 0) {
            const years = [...new Set(regionalData.map(d => d.year))];
            minYear = Math.min(...years);
            maxYear = Math.max(...years);
            if (!yearRange[0]) yearRange = [minYear, maxYear];
        }
    }

    // 修改过滤逻辑以支持时间范围
    $: filteredData = regionalData.filter(d => {
        if (!d || !d.year || !d.sector || !d.region) return false;
        if (d.region === "其他" || d.region === "Others") return false;

        if (isTimeRange) {
            return d.year >= yearRange[0] && d.year <= yearRange[1];
        } else {
            return selectedYear === 'All' || +d.year === +selectedYear;
        }
    });

    // Calculate sector summaries
    $: sectorAnalysis = d3.rollup(filteredData,
        v => d3.sum(v, d => d.count), // Sum the counts instead of counting items
        d => d.sector,
        d => d.region
    );
    
    // Get top regions for each sector
    $: topRegionsBySector = Array.from(sectorAnalysis).map(([sector, regions]) => {
        const regionEntries = Array.from(regions);
        const totalSectorCount = d3.sum(regionEntries, d => d[1]);
        
        const sortedRegions = regionEntries
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([region, count]) => ({
                region,
                count,
                percentage: ((count / totalSectorCount) * 100).toFixed(1)
            }));

        return { sector, topRegions: sortedRegions };
    });

    // Group sectors into rows of 4
    $: sectorRows = topRegionsBySector.reduce((rows, sector, index) => {
        if (index % 4 === 0) rows.push([]);
        rows[rows.length - 1].push(sector);
        return rows;
    }, []);

    $: console.log('Filtered Data Sample:', filteredData.slice(0, 5));
    $: console.log('Sector Analysis:', topRegionsBySector);
</script>

<div class="regional-analysis">
    <div class="controls">
        <div class="time-control">
            <label class="toggle">
                <input 
                    type="checkbox" 
                    bind:checked={isTimeRange}
                >
                <span class="toggle-label">Click to select Time Period</span>
            </label>

            {#if isTimeRange}
                <div class="range-slider">
                    <div class="year-labels">
                        <span>{yearRange[0]}</span>
                        <span>{yearRange[1]}</span>
                    </div>
                    <div class="slider-container">
                        <input 
                            type="range" 
                            min={minYear} 
                            max={maxYear} 
                            step="1"
                            bind:value={yearRange[0]}
                            class="slider slider-1"
                        >
                        <input 
                            type="range" 
                            min={minYear} 
                            max={maxYear} 
                            step="1"
                            bind:value={yearRange[1]}
                            class="slider slider-2"
                        >
                    </div>
                </div>
            {:else}
                <select bind:value={selectedYear}>
                    <option value="All">All Years</option>
                    {#each [...new Set(regionalData.map(d => d.year))].sort() as year}
                        <option value={year}>{year}</option>
                    {/each}
                </select>
            {/if}
        </div>
    </div>

    {#if filteredData.length === 0}
        <p>No data available for the selected filters</p>
    {:else}
        <SectorRegionBarChart 
            data={filteredData}
            {selectedYear}
            {selectedSector}
        />

        <div class="sectors-grid">
            {#each sectorRows as row}
                <div class="sector-row">
                    {#each row as {sector, topRegions}}
                        <div class="sector-card">
                            <h4>{sector}</h4>
                            <ul class="region-list">
                                {#each topRegions as {region, count, percentage}}
                                    <li>
                                        <span class="region">{region}:</span>
                                        <div class="stats">
                                            <span class="count">{count}</span>
                                            <span class="percentage">({percentage}%)</span>
                                        </div>
                                    </li>
                                {/each}
                            </ul>
                        </div>
                    {/each}
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    .regional-analysis {
        padding: 1rem;
    }

    .sectors-grid {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .sector-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
    }

    .sector-card {
        background: white;
        padding: 1.25rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #eee;
    }

    .sector-card h4 {
        margin: 0 0 1rem 0;
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 600;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.5rem;
    }

    .region-list {
        list-style-type: none;
        padding: 0;
        margin: 0;
        font-size: 0.9rem;
    }

    .region-list li {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.4rem 0;
        border-bottom: 1px solid #f0f0f0;
    }

    .region-list li:last-child {
        border-bottom: none;
    }

    .region {
        font-weight: 500;
        color: #444;
        flex: 1;
    }

    .count {
        color: #2c3e50;
        margin-right: 0.5rem;
    }

    .percentage {
        color: #666;
        min-width: 4rem;
        text-align: right;
    }

    /* Responsive design */
    @media (max-width: 1400px) {
        .sector-row {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    @media (max-width: 1000px) {
        .sector-row {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 600px) {
        .sector-row {
            grid-template-columns: 1fr;
        }
    }

    .controls {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
    }

    .time-control {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .toggle {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
    }

    .toggle-label {
        color: #2c3e50;
        font-weight: 500;
    }

    .range-slider {
        width: 300px;
        padding: 0 1rem;
    }

    .year-labels {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        color: #666;
    }

    input[type="range"] {
        width: 100%;
        margin: 0.5rem 0;
    }

    select {
        padding: 0.5rem;
        border-radius: 4px;
        border: 1px solid #ddd;
        background: white;
        min-width: 150px;
    }

    /* 美化 range slider */
    input[type="range"] {
        -webkit-appearance: none;
        height: 4px;
        background: #ddd;
        border-radius: 2px;
    }

    input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 16px;
        height: 16px;
        background: #4a90e2;
        border-radius: 50%;
        cursor: pointer;
    }

    input[type="range"]:focus {
        outline: none;
    }
</style>