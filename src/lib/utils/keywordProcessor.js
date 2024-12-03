import * as d3 from 'd3';

/**
 * @typedef {Object} KeywordData
 * @property {string} word
 * @property {number} frequency
 * @property {Array<{year: number, count: number}>} timeDistribution
 */

/**
 * 从原始数据中提取关键词
 * @param {Array} newsData
 * @returns {Array<KeywordData>}
 */
export function extractKeywords(newsData) {
  // 扩展技术领域关键词
  const techKeywords = {
    '新能源': [
      '新能源', '清洁能源', '可再生能源', '光伏', '风电', '氢能',
      '新能源汽车', '电动汽车', '充电桩', '动力电池'
    ],
    '人工智能': [
      '人工智能', 'AI', '机器学习', '深度学习', '智能化', 
      '神经网络', '算法', '智能系统', '自然语言处理'
    ],
    '芯片半导体': [
      '芯片', '半导体', '集成电路', 'IC', '晶圆', 
      '光刻机', '封装测试', '存储器', '处理器'
    ],
    '数字经济': [
      '数字经济', '数字化转型', '智慧城市', '数字人民币',
      '电子商务', '互联网经济', '平台经济', '数字贸易'
    ],
    '航空航天': [
      '航空', '航天', '卫星', '火箭', '空间站',
      '运载火箭', '探测器', '航天器', '商业航天'
    ],
    '智能制造': [
      '智能制造', '工业互联网', '机器人', '自动化',
      '工业4.0', '智能工厂', '数字化工厂', '柔性制造'
    ],
    '生物医药': [
      '生物技术', '生物医药', '疫苗', '基因', '医疗科技',
      '创新药', '细胞治疗', '基因编辑', '生物制品'
    ],
    '新材料': [
      '新材料', '碳纤维', '石墨烯', '纳米材料',
      '特种材料', '高性能材料', '复合材料', '前沿材料'
    ],
    '量子科技': [
      '量子计算', '量子通信', '量子科技', '量子力学',
      '量子密钥', '量子芯片', '量子领域', '量子技术'
    ],
    '区块链': [
      '区块链', '加密货币', '比特币', '数字货币',
      '分布式账本', '智能合约', '数字资产', '链上'
    ],
    '通信技术': [
      '5G', '6G', '通信技术', '移动通信',
      '基站', '网络设备', '通信网络', '宽带'
    ],
    '大数据云计算': [
      '大数据', '云计算', '数据中心', '云服务',
      '数据分析', '云平台', '边缘计算', '数据处理'
    ]
  };

  const keywordMap = new Map();

  // 添加调试日志
  console.log('Processing news data:', newsData?.slice(0, 3));

  // 处理每条新闻
  newsData.forEach(news => {
    if (!news || !news.date || !news.title || !news.content) {
      console.warn('Skipping invalid news item:', news);
      return;
    }

    const text = `${news.title} ${news.content}`;
    const year = parseInt(news.date.substring(0, 4));

    // 检查每个技术领域的关键词
    for (const [category, keywords] of Object.entries(techKeywords)) {
      // 计算该新闻中包含的关键词数量
      const matchedKeywords = keywords.filter(keyword => text.includes(keyword));
      
      if (matchedKeywords.length > 0) {
        if (!keywordMap.has(category)) {
          keywordMap.set(category, {
            word: category,
            frequency: 0,
            matchedTerms: new Set(), // 记录匹配到的具体关键词
            timeDistribution: new Map(),
            regions: new Map() // 添加地区分布统计
          });
        }

        const keywordData = keywordMap.get(category);
        keywordData.frequency += 1;
        matchedKeywords.forEach(term => keywordData.matchedTerms.add(term));

        // 更新时间分布
        const yearCount = keywordData.timeDistribution.get(year) || 0;
        keywordData.timeDistribution.set(year, yearCount + 1);

        // 更新地区分布
        if (news.region) {
          const regionCount = keywordData.regions.get(news.region) || 0;
          keywordData.regions.set(news.region, regionCount + 1);
        }
      }
    }
  });

  // 添加调试日志
  console.log('Extracted keyword map:', Array.from(keywordMap.entries()));

  // 转换数据格式并按频率排序
  return Array.from(keywordMap.values())
    .map(data => ({
      word: data.word,
      frequency: data.frequency,
      timeDistribution: Array.from(data.timeDistribution.entries())
        .map(([year, count]) => ({ year, count }))
        .sort((a, b) => a.year - b.year)
    }))
    .sort((a, b) => b.frequency - a.frequency);
}

/**
 * 从文本中提取关键词
 * @param {string} text
 * @returns {Array<string>}
 */
function extractKeywordsFromText(text) {
  if (!text) return [];
  
  return text.split(/[,\s]+/)
    .map(word => word.trim())
    .filter(word => word.length > 1)
    .filter(word => !isStopWord(word));
}

/**
 * 检查是否为停用词
 * @param {string} word
 * @returns {boolean}
 */
function isStopWord(word) {
  const stopWords = new Set([
    'and', 'or', 'the', 'a', 'an', 'of', 'to', 'in', 'for',
    '和', '与', '及', '等', '的', '了', '在', '是'
  ]);
  return stopWords.has(word.toLowerCase());
}

/**
 * 获取关键词的时间序列数据
 * @param {string} keyword
 * @param {Array<KeywordData>} keywordData
 * @returns {Array<{year: number, count: number}>}
 */
export function getKeywordTimeSeries(keyword, keywordData) {
  const data = keywordData.find(d => d.word === keyword);
  return data ? data.timeDistribution : [];
}

/**
 * 获取搜索建议
 * @param {string} searchTerm
 * @param {Array<KeywordData>} keywordData
 * @param {number} maxSuggestions
 * @returns {Array<string>}
 */
export function getSuggestions(searchTerm, keywordData, maxSuggestions = 5) {
  if (!searchTerm) return [];
  
  const normalizedSearch = searchTerm.toLowerCase();
  
  return keywordData
    .filter(data => data.word.toLowerCase().includes(normalizedSearch))
    .sort((a, b) => b.frequency - a.frequency)
    .slice(0, maxSuggestions)
    .map(data => data.word);
}