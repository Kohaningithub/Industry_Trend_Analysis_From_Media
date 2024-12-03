<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { slide } from 'svelte/transition';
  import KeywordTrendChart from './KeywordTrendChart.svelte';
  const dispatch = createEventDispatcher();

  export let data;
  export let keywordData;
  export let searchTerm = '';
  export let suggestions = [];
  export let selectedKeyword = null;
  export let timeSeriesData = [];
  export let placeholder = "Search for keywords...";

  let searchInput;
  let showSuggestions = false;

  // 处理关键词选择
  function handleKeywordSelect(keyword) {
    selectedKeyword = keyword;
    searchTerm = keyword;
    showSuggestions = false;
    dispatch('select', { keyword });
  }

  // 获取热门关键词
  $: popularKeywords = keywordData
    ?.slice(0, 5)
    ?.map(k => k.word) || [];

  $: trendData = selectedKeyword ? 
    keywordData.find(d => d.word === selectedKeyword)?.timeDistribution || [] : [];
</script>

<div class="keyword-explorer">
  <div class="search-container">
    <input
      type="text"
      bind:value={searchTerm}
      {placeholder}
      bind:this={searchInput}
      on:focus={() => showSuggestions = true}
    />
    
    {#if showSuggestions && suggestions.length > 0}
      <div class="suggestions" transition:slide>
        {#each suggestions as suggestion}
          <button 
            class="suggestion-item"
            on:click={() => handleKeywordSelect(suggestion)}
          >
            {suggestion}
          </button>
        {/each}
      </div>
    {/if}
  </div>

  <div class="popular-keywords">
    <h3>Popular Keywords:</h3>
    <div class="keyword-chips">
      {#each popularKeywords as keyword}
        <button 
          class="keyword-chip"
          on:click={() => handleKeywordSelect(keyword)}
        >
          {keyword}
        </button>
      {/each}
    </div>
  </div>

  {#if selectedKeyword && trendData.length}
    <KeywordTrendChart 
      data={trendData}
      selectedKeyword={selectedKeyword}
    />
  {/if}
</div>

<style>
  .keyword-explorer {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }

  .search-container {
    position: relative;
    margin-bottom: 1rem;
  }

  input {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }

  .suggestions {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #ddd;
    border-top: none;
    border-radius: 0 0 4px 4px;
    max-height: 200px;
    overflow-y: auto;
    z-index: 1000;
  }

  .suggestion-item {
    width: 100%;
    padding: 0.5rem 1rem;
    border: none;
    background: none;
    text-align: left;
    cursor: pointer;
  }

  .suggestion-item:hover {
    background: #f5f5f5;
  }

  .popular-keywords {
    margin-top: 1rem;
  }

  .keyword-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }

  .keyword-chip {
    padding: 0.5rem 1rem;
    background: #e3f2fd;
    border: none;
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .keyword-chip:hover {
    background: #bbdefb;
  }
</style>