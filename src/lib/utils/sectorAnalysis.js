function getTopRegionsPerSector(data) {
    // Group data by sector and count region occurrences
    const sectorRegionCounts = d3.rollup(data,
        v => d3.rollup(v, g => g.length, d => d.region),  // Count occurrences of each region
        d => d.sector                                      // Group by sector
    );

    // Convert to more usable format and sort
    const results = Array.from(sectorRegionCounts).map(([sector, regionCounts]) => {
        const topRegions = Array.from(regionCounts)
            .sort((a, b) => b[1] - a[1])                  // Sort by count descending
            .slice(0, 5);                                 // Get top 5 regions

        return {
            sector,
            regions: topRegions.map(([region, count]) => ({
                region,
                count,
                percentage: (count / d3.sum(regionCounts.values()) * 100).toFixed(1)
            }))
        };
    });

    return results;
}