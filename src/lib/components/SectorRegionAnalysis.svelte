<script>
    export let data;
    
    const topRegionsPerSector = getTopRegionsPerSector(data);
</script>

<div class="analysis">
    {#each topRegionsPerSector as {sector, regions}}
        <div class="sector">
            <h3>{sector}</h3>
            <ul>
                {#each regions as {region, count, percentage}}
                    <li>{region}: {count} mentions ({percentage}%)</li>
                {/each}
            </ul>
        </div>
    {/each}
</div>

<style>
    .analysis {
        display: grid;
        gap: 1rem;
    }
    .sector {
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
</style>