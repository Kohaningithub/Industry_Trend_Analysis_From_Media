<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import { loadData } from './lib/utils/dataProcessor';
  import TimeSeriesChart from './lib/components/TimeSeriesChart.svelte';
  import HeatMap from './lib/components/HeatMap.svelte';
  import ComparisonChart from './lib/components/ComparisonChart.svelte';
  import RegionalAnalysis from './lib/components/RegionalAnalysis.svelte';
  import SectorRegionBarChart from './lib/components/SectorRegionBarChart.svelte';
  import RegionalTemporal from './lib/components/RegionalTemporal.svelte';

  let data = [];
  let activeSection = 'overview';
  let regionalData = [];
  let selectedYear = 2023;
  let selectedSector = 'All';
  let explorationView = 'regional';

  onMount(async () => {
    try {
      data = await loadData();
      const response = await fetch('data/processed_regional_data.csv');
      const csvText = await response.text();
      
      // Parse CSV with explicit column mapping and proper count handling
      regionalData = d3.csvParse(csvText, d => ({
        year: +d.Year || +d.year,
        sector: d.Industry || d.industry || d.sector,
        region: d.Region || d.region,
        count: +(d.Frequency || d.frequency || 1)
      }));

      // Validate and filter out invalid entries
      regionalData = regionalData.filter(d => 
        d.year && 
        d.sector && 
        d.region && 
        !isNaN(d.count) && 
        d.count > 0
      );

      console.log('Sample of parsed data with counts:', 
        regionalData.slice(0, 5).map(d => ({
          year: d.year,
          sector: d.sector,
          region: d.region,
          count: d.count
        }))
      );

    } catch (error) {
      console.error('Error loading data:', error);
    }
  });

</script>

<main>
  <nav class="dashboard-nav">
    <button 
      class:active={activeSection === 'overview'} 
      on:click={() => activeSection = 'overview'}
    >
      Overview
    </button>
    <button 
      class:active={activeSection === 'exploration'} 
      on:click={() => activeSection = 'exploration'}
    >
      Detailed Exploration
    </button>
    <button 
      class:active={activeSection === 'story'} 
      on:click={() => activeSection = 'story'}
    >
      Story & Context
    </button>
  </nav>

  {#if data.length}
    {#if activeSection === 'overview'}
      <section class="overview-section">
        <h1>Industrial Policy Focus Analysis: Xinwenlianbo Coverage Patterns</h1>
        
        <div class="methodology-note">
          <h3>Analysis Strategy</h3>
          <p>This analysis tracks the frequency of sector mentions in Xinwenlianbo (新闻联播), 
          China's primary state television news program, to reveal subtle shifts in industrial policy focus. 
          By analyzing coverage patterns across different technological sectors, we can observe how policy 
          priorities evolve even when explicit policy statements change.</p>
        </div>

        <!-- Enhanced Key Findings Summary -->
        <div class="key-findings">
          <h2>Key Findings</h2>
          <ul>
            <li>Aerospace and Electric Power maintain prominent coverage in state media</li>
            <li>Coverage of technological sectors in Xinwenlianbo remained robust after March 2019</li>
            <li>Post-2021 period shows heightened focus on multiple strategic sectors</li>
            <li>New Energy Vehicles received increasing media attention in recent years</li>
          </ul>
        </div>

        <!-- Interactive Guide -->
        <div class="visualization-guide">
          <h3>How to Use These Visualizations</h3>
          <ol>
            <li>Start with the Time Series to identify major trends and peaks in coverage</li>
            <li>Use the Heat Map to see intensity patterns across all sectors simultaneously</li>
            <li>Compare pre/post-2019 patterns in the Comparison Chart to understand policy impact</li>
          </ol>
        </div>

        <!-- Time Series with Enhanced Context -->
        <div class="time-series-section">
          <h2>Time Series Analysis</h2>
          <p class="description">Track coverage shifts across technological sectors, with notable increases post-2021 as China emphasized technological self-reliance during post-COVID recovery.</p>
          <p class="instructions">Compare sectors using checkboxes, and drag to zoom into specific time periods.</p>
          <TimeSeriesChart {data} />
        </div>

        <!-- Heat Map with COVID Context -->
        <div class="pattern-section">
          <h2>Heat Map Visualization</h2>
          <p>Sector coverage patterns reveal interesting shifts, particularly after 2021.</p>
          <div class="context-note">
            <h4>Post-COVID Recovery Period (2021 onwards)</h4>
            <p>The intensification of coverage (darker blues) across sectors after 2021 coincides with China's post-COVID recovery phase:</p>
            <ul>
              <li>Increased emphasis on technological self-reliance</li>
              <li>Focus on supply chain resilience</li>
              <li>Acceleration of digital transformation initiatives</li>
            </ul>
          </div>
          <HeatMap {data} />
        </div>

        <!-- Revised Impact Analysis -->
        <div class="impact-section">
          <h2>March 2019 Coverage Pattern Analysis</h2>
          <p>Analysis of Xinwenlianbo coverage reveals that despite the shift away from explicit MIC2025 
          terminology in official speeches, state media attention to key technological sectors remained consistent:</p>
          <div class="analysis-points">
            <ul>
              <li>Maintained or increased coverage across strategic sectors</li>
              <li>Aerospace sector received enhanced media attention</li>
              <li>Consistent coverage of core technological areas</li>
              <li>Sustained policy focus through media representation</li>
            </ul>
            <div class="note-box">
              <p><strong>Note:</strong> In March 2019, during the opening session of China's National People's Congress, 
                Premier Li Keqiang notably omitted any mention of the "Made in China 2025" (MIC2025) initiative in his 
                annual government work report—the first such omission since the plan's introduction in 2015. Many analysts 
                and reports suggest that "Made in China 2025" continues in substance though not in name. While explicit 
                references to "Made in China 2025" decreased in official speeches after 
                March 2019, Xinwenlianbo's coverage of key technological sectors remained robust, suggesting continuity in 
                industrial policy priorities through different communication channels.</p>
              </div>
          </div>
          <ComparisonChart {data} />
        </div>

        <!-- Add back the Enhanced Context Box -->
        <section class="info-box">
          <h3>Understanding Key Transitions</h3>
          <div class="context-content">
            <div class="policy-context">
              <h4>Policy Communication Evolution:</h4>
              <ul>
                <li><strong>2015-2019:</strong> Direct MIC2025 references in policy</li>
                <li><strong>March 2019:</strong> Shift in communication style, not substance</li>
                <li><strong>2020-2021:</strong> COVID-19 impact period</li>
                <li><strong>Post-2021:</strong> Renewed technological focus</li>
              </ul>
            </div>
          </div>
        </section>
      </section>
    {:else if activeSection === 'exploration'}
      <section class="exploration-section">
        <h1>Detailed Regional and Sectoral Analysis</h1>
        
        <div class="exploration-nav">
          <button 
            class:active={explorationView === 'regional'} 
            on:click={() => explorationView = 'regional'}
          >
            Regional Distribution
          </button>
          <button 
            class:active={explorationView === 'temporal'} 
            on:click={() => explorationView = 'temporal'}
          >
            Temporal Changes
          </button>
        </div>

        <div class="methodology-note">
          <h3>Regional Analysis Approach</h3>
          <p>This section examines the geographical distribution of industrial policy focus across China's regions,
             revealing patterns of regional specialization and policy implementation.</p>
        </div>

        {#if explorationView === 'regional'}
          <div class="regional-analysis-container">
            <h2>Regional Distribution of Technology Sectors</h2>
            
            <div class="analysis-guide">
              <h3>How to Explore This Data</h3>
              <p>This interactive visualization reveals the geographic distribution of China's technological development focus across different sectors. Use the time period selector to uncover patterns:</p>
              
              <div class="exploration-tips">
                <h4>Key Questions to Explore:</h4>
                <ul>
                  <li>Which regions lead in specific technological sectors?</li>
                  <li>How has regional specialization evolved over time?</li>
                  <li>Are there clusters of technological development in particular areas?</li>
                </ul>
              </div>

              <div class="interpretation-guide">
                <h4>Understanding the Visualization:</h4>
                <ol>
                  <li><strong>Time Period Selection:</strong> Use the slider to compare different time periods and observe how regional leadership has shifted.</li>
                  <li><strong>Bar Length:</strong> Represents the number of mentions in state media, indicating policy attention and development focus.</li>
                </ol>
              </div>
            </div>

            <RegionalAnalysis 
              {regionalData}
              {selectedYear}
              {selectedSector}
            />

            <div class="analysis-insights">
              <h4>Key Patterns to Notice:</h4>
              <ul>
                <li><strong>Beijing's Dominance:</strong> Leads in multiple high-tech sectors, particularly in Information Technology and New Energy Vehicles.</li>
                <li><strong>Regional Specialization:</strong> Some regions show strong focus in specific sectors (e.g., Shanghai in Ocean Engineering).</li>
                <li><strong>Development Clusters:</strong> Coastal regions generally show higher technological activity across sectors.</li>
              </ul>
            </div>

            <div class="research-directions">
              <h4>Further Research Directions:</h4>
              <p>Consider exploring these aspects in your analysis:</p>
              <ul>
                <li>Compare regional specialization with local economic policies and industrial bases</li>
                <li>Investigate the relationship between regional focus and local innovation outcomes</li>
                <li>Analyze how regional competition or cooperation affects technological development</li>
                <li>Examine the impact of national initiatives on regional technological focus</li>
              </ul>
            </div>
          </div>
        {:else if explorationView === 'temporal'}
          <div class="temporal-analysis-container">
            <h2>Temporal Evolution of Regional Technology Development</h2>
            
            <!-- Add narrative introduction -->
            <div class="analysis-guide">
              <h3>Exploring Technology Development Over Time</h3>
              <p>This visualization tracks how different regions and sectors have evolved over time, revealing the dynamic nature of China's technological development landscape:</p>
              
              <div class="exploration-tips">
                <h4>Interactive Features:</h4>
                <ul>
                  <li>Use the Region selector to focus on specific areas or view nationwide trends</li>
                  <li>Switch between sectors to compare different technology domains</li>
                </ul>
              </div>

              <!-- Moved RegionalTemporal component here -->
              <RegionalTemporal {regionalData} />

              <div class="interpretation-guide">
                <h4>Reading the Trends:</h4>
                <ol>
                  <li>Select a specific region (e.g., "Beijing") to see all its industry developments over time</li>
                  <li>Notice which industries are prominent in this region</li>
                  <li>Select a specific industry to focus on its development trajectory</li>
                </ol>
              </div>

              <div class="analysis-insights">
                <h4>Notable Patterns:</h4>
                <ul>
                  <li><strong>Post-2020 Acceleration:</strong> Many sectors show increased momentum after the pandemic</li>
                  <li><strong>Regional Specialization:</strong> Different regions show distinct temporal patterns in their focus sectors</li>
                </ul>
              </div>

              <div class="research-directions">
                <h4>Research Opportunities:</h4>
                <p>Consider these angles for deeper analysis:</p>
                <ul>
                  <li>Investigate the relationship between regional policy changes and sector growth patterns</li>
                  <li>Analyze how external events (trade policies, global events) impact development trajectories</li>
                  <li>Compare development speeds and patterns across different regions</li>
                  <li>Identify successful development models by studying leading regions' temporal patterns</li>
                </ul>
              </div>

              <div class="key-events-timeline">
                <h4>Key Timeline Events:</h4>
                <ul>
                  <li><strong>2015-2016:</strong> Initial phase of technological development focus</li>
                  <li><strong>2019:</strong> Policy adjustment period with shifts in development emphasis</li>
                  <li><strong>2020-2021:</strong> Post-pandemic acceleration in technological development</li>
                  <li><strong>2022-2023:</strong> Enhanced focus on self-reliance and innovation</li>
                </ul>
              </div>
            </div>
          </div>
        {/if}
      </section>
    {:else if activeSection === 'story'}
      <section class="story-section">
        <h1>Story & Context</h1>
        
        <div class="context-background">
          <h2>Policy Evolution Context</h2>
          <p>As China approaches the 2025 milestone of "Made in China 2025," this analysis reveals a fascinating 
          transformation in how industrial policy is communicated. Despite reduced explicit references since 2018, 
          our data shows continued and possibly accelerated implementation across key sectors.</p>
          
          <div class="policy-shift-box">
            <h3>The "Policy in Silence" Phenomenon</h3>
            <ul>
              <li>Reduced explicit "Made in China 2025" references in official communications post-2018</li>
              <li>Continued implementation through alternative communication channels</li>
              <li>Sustained focus on strategic sectors despite changed rhetoric</li>
            </ul>
          </div>
        </div>

        <div class="key-insights">
          <h2>Key Insights</h2>
          
          <div class="insight-card">
            <h3>Media Coverage Patterns</h3>
            <ul>
              <li>Consistent coverage of core technological sectors despite reduced policy mentions</li>
              <li>Strategic shift in communication style while maintaining policy substance</li>
              <li>Increased emphasis on domestic innovation and self-reliance narratives</li>
            </ul>
          </div>

          <div class="insight-card">
            <h3>Sector-Specific Trends</h3>
            <ul>
              <li>Enhanced focus on semiconductor and AI sectors post-2020</li>
              <li>Sustained attention to new energy vehicles and renewable energy</li>
              <li>Growing emphasis on digital economy and smart manufacturing</li>
            </ul>
          </div>

          <div class="insight-card">
            <h3>Policy Implementation Indicators</h3>
            <ul>
              <li>Correlation between media coverage intensity and sector development</li>
              <li>Adaptive policy messaging responding to international dynamics</li>
              <li>Regional variations in sector emphasis and development focus</li>
            </ul>
          </div>
        </div>

        <div class="research-implications">
          <h2>Research Implications</h2>
          <p>This analysis demonstrates the value of media coverage analysis in understanding China's industrial 
          policy evolution, particularly when traditional policy documents become less explicit. The findings 
          suggest that while the communication strategy has evolved, the fundamental focus on technological 
          self-reliance and industrial upgrading remains consistent.</p>
        </div>
      </section>
    {/if}
  {:else}
    <p class="loading">Loading data...</p>
  {/if}
</main>
<style>
  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  section {
    margin: 2rem 0;
    padding: 1rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .info-box {
    background: #f5f5f5;
    padding: 2rem;
    text-align: center;
    margin-top: 2rem;
    border-radius: 8px;
    max-width: 600px;
    margin: 2rem auto;
  }

  .info-box h3 {
    margin-bottom: 1.5rem;
  }

  .context-content {
    display: flex;
    justify-content: center;
    width: 100%;
  }

  .policy-context {
    background: #fff;
    padding: 2rem;
    border-radius: 8px;
    max-width: 600px;
    margin: 0 auto;
  }

  .policy-context h4 {
    text-align: center;
    margin-bottom: 1rem;
  }

  .policy-context ul {
    list-style-type: none;
    padding: 0;
    text-align: left;
  }

  .policy-context li {
    margin: 0.75rem 0;
  }

  h1 {
    text-align: center;
    margin-bottom: 2rem;
  }

  h2 {
    color: #333;
    margin-bottom: 1rem;
  }

  p {
    color: #666;
    line-height: 1.6;
  }

  .loading {
    text-align: center;
    font-size: 1.2rem;
    color: #666;
    padding: 2rem;
  }

  .time-series-section h2 {
    margin-bottom: 8px;  /* Reduce space after heading */
  }

  .description {
    margin: 0 0 4px 0;  /* Reduce space between paragraphs */
  }

  .instructions {
    margin: 0 0 12px 0;  /* Add some space before the chart */
  }

  .dashboard-nav {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .dashboard-nav button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    background: #f5f5f5;
    cursor: pointer;
    transition: all 0.2s;
  }

  .dashboard-nav button.active {
    background: #333;
    color: white;
  }

  .key-findings {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
  }

  .key-findings ul {
    list-style-type: none;
    padding: 0;
  }

  .key-findings li {
    padding: 0.5rem 0;
    padding-left: 1.5rem;
    position: relative;
  }

  .key-findings li:before {
    content: "→";
    position: absolute;
    left: 0;
    color: #666;
  }
  .context-note {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 4px solid #4a90e2;
  }

  .transition-points {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 1rem 0;
  }

  .transition {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
  }

  .analysis-points {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
  }

  .analysis-points ul {
    list-style-type: none;
    padding-left: 0;
  }

  .analysis-points li {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
    position: relative;
  }

  .analysis-points li:before {
    content: "•";
    position: absolute;
    left: 0;
    color: #4a90e2;
  }

  .note-box {
    background: #fff;
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
    border-left: 4px solid #ffd700;
  }

  .methodology-note {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0 2rem 0;
    border-left: 4px solid #2c3e50;
  }

  .methodology-note p {
    margin: 0.5rem 0 0 0;
    color: #445;
    line-height: 1.6;
  }

  .regional-analysis-container,
  .regional-heatmap-container {
    margin: 2rem 0;
    padding: 1.5rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .regional-analysis-container h2,
  .regional-heatmap-container h2 {
    color: #333;
    margin-bottom: 1rem;
  }

  .description {
    color: #666;
    margin-bottom: 1.5rem;
  }

  .controls {
    display: flex;
    gap: 2rem;
    margin: 1rem 0;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
    align-items: center;
    justify-content: center;
  }

  .controls label {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .controls select {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ddd;
  }

  .exploration-nav {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 1rem 0 2rem 0;
  }

  .exploration-nav button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    background: #f5f5f5;
    cursor: pointer;
    transition: all 0.2s;
  }

  .exploration-nav button.active {
    background: #4a90e2;
    color: white;
  }

  .exploration-section {
    padding: 1rem;
  }

  .analysis-guide {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0 2rem 0;
  }

  .exploration-tips,
  .interpretation-guide,
  .analysis-insights,
  .research-directions {
    margin: 1.5rem 0;
    padding: 1rem;
    background: white;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }

  .interpretation-guide ol,
  .exploration-tips ul,
  .analysis-insights ul,
  .research-directions ul {
    padding-left: 1.5rem;
  }

  .interpretation-guide li,
  .exploration-tips li,
  .analysis-insights li,
  .research-directions li {
    margin: 0.5rem 0;
    line-height: 1.6;
  }

  .analysis-insights strong {
    color: #4a90e2;
  }

  .research-directions {
    border-left: 4px solid #4a90e2;
  }

  .temporal-analysis-container {
    margin: 2rem 0;
    padding: 1.5rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .key-events-timeline {
    margin: 1.5rem 0;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 6px;
    border-left: 4px solid #ffd700;
  }

  .key-events-timeline ul {
    list-style-type: none;
    padding-left: 0;
  }

  .key-events-timeline li {
    margin: 0.8rem 0;
    padding-left: 1.5rem;
    position: relative;
  }

  .key-events-timeline li:before {
    content: "•";
    position: absolute;
    left: 0;
    color: #ffd700;
    font-weight: bold;
  }

  .key-events-timeline strong {
    color: #2c3e50;
  }

  /* Add this style to ensure proper spacing around the plot */
  :global(.temporal-analysis-container .RegionalTemporal) {
    margin: 2rem 0;
    padding: 1rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }

  .story-section {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  .context-background, .key-insights, .research-implications {
    margin: 2rem 0;
    padding: 1.5rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .policy-shift-box {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 6px;
    margin: 1rem 0;
    border-left: 4px solid #4a90e2;
  }

  .insight-card {
    background: #f8f9fa;
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 6px;
    border-left: 4px solid #2ecc71;
  }

  .insight-card h3 {
    color: #2c3e50;
    margin-top: 0;
  }

  .insight-card ul {
    list-style-type: none;
    padding-left: 0;
  }

  .insight-card li {
    margin: 0.8rem 0;
    padding-left: 1.5rem;
    position: relative;
  }

  .insight-card li:before {
    content: "→";
    position: absolute;
    left: 0;
    color: #2ecc71;
  }

  .research-implications {
    border-left: 4px solid #3498db;
    background: #f8f9fa;
  }

</style>

