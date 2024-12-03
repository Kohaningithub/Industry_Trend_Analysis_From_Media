import * as XLSX from 'xlsx';

export async function loadData() {
    try {
        const response = await fetch('/data/combined_frequency_data_english.csv');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const text = await response.text();
        const lines = text.trim().split('\n');
        
        // Skip header and process data
        const data = lines.slice(1)
            .map(line => {
                const [sector, month, frequency, year] = line.split(',');
                const item = {
                    sector: sector.trim(),
                    month: parseInt(month, 10),
                    frequency: parseInt(frequency, 10),
                    year: parseInt(year, 10)
                };
                
                // Debug log each processed item
                console.log('Processing:', item);
                return item;
            })
            .filter(item => 
                item.sector && 
                !isNaN(item.month) && 
                !isNaN(item.frequency) && 
                !isNaN(item.year)
            );

        // Log the first few processed items
        console.log('First 5 processed items:', data.slice(0, 5));
        
        return data;
    } catch (error) {
        console.error('Error loading data:', error);
        throw error;
    }
}

export async function loadNewsData() {
  try {
    const response = await fetch('data/china_nightly_news_2023.xlsx');
    const arrayBuffer = await response.arrayBuffer();
    const workbook = XLSX.read(arrayBuffer);

    // 获取第一个工作表
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    
    // 转换为JSON
    const jsonData = XLSX.utils.sheet_to_json(worksheet, {
      header: ['date', 'title', 'content', 'region'],
      range: 1  // 跳过标题行
    });
    
    return jsonData;
  } catch (error) {
    console.error('Error loading news data:', error);
    return [];
  }
}