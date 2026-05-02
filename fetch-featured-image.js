/**
 * AI News Publisher - Featured Image Fetcher (v1.1)
 * Improved keyword extraction and query building
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, 'data');
const cacheDir = join(dataDir, 'images');
mkdirSync(cacheDir, { recursive: true });

const config = {
  pexels: {
    enabled: !!process.env.WECHAT_PEXELS_API_KEY,
    apiKey: process.env.WECHAT_PEXELS_API_KEY || '',
    perPage: 5
  },
  cache: {
    dir: cacheDir,
    ttlDays: 30
  }
};

/**
 * 提取并优化关键词
 */
function extractKeywords(title) {
  // 实体词典（优先级）
  const entityPriorities = {
    '五角大楼': 10, 'Pentagon': 10, 'DoD': 10, '国防部': 10,
    '英伟达': 9, 'Nvidia': 9,
    '微软': 8, 'Microsoft': 8,
    'AWS': 8, 'Amazon': 8, '亚马逊': 8,
    'Meta': 8, 'Facebook': 7,
    'OpenAI': 9, ' Musk': 8, '马斯克': 8,
    'Altman': 8, '阿尔特曼': 8,
    '机器人': 7, 'robotics': 7, '机器人': 7,
    '树莓派': 6, 'Raspberry Pi': 6,
    'Hacker News': 6, 'HN': 5,
    'TechCrunch': 5
  };

  // 提取提及的实体
  const foundEntities = [];
  for (const [entity, priority] of Object.entries(entityPriorities)) {
    if (title.includes(entity)) {
      foundEntities.push({ name: entity, priority });
    }
  }

  // 按优先级排序，取最高3个
  foundEntities.sort((a, b) => b.priority - a.priority);
  const topEntities = foundEntities.slice(0, 3).map(e => e.name);

  // 提取英文关键词
  const englishWords = (title.match(/[A-Za-z]{4,}/g) || [])
    .filter(w => !['news', 'article', 'blog'].includes(w.toLowerCase()))
    .slice(0, 3);

  // 提取中文关键词
  const chineseKeywords = (title.match(/[\u4e00-\u9fa5]{2,}/g) || []).slice(0, 2);

  // 构建搜索查询（去重 + 优化）
  let queryParts = [];

  // 优先级 1：实体（英文优先，更易搜索）
  const uniqueEntities = [...new Set(topEntities)];
  for (const e of uniqueEntities) {
    // 如果实体是中文，尝试找对应的英文别名
    const enAlias = entityPriorities[Object.keys(entityPriorities).find(k => k === e && /[\u4e00-\u9fa5]/.test(k) ? Object.values(entityPriorities)[Object.keys(entityPriorities).indexOf(k)] : null)];
    // 简单起见，直接使用 entity（英文实体直接搜索，中文实体可能需要映射）
    if (/^[A-Za-z]/.test(e)) {
      queryParts.push(e);
    }
  }

  // 优先级 2：英文关键词
  for (const w of englishWords) {
    if (!queryParts.join(' ').toLowerCase().includes(w.toLowerCase())) {
      queryParts.push(w);
    }
  }

  // 去重
  const uniqueParts = [...new Set(queryParts)];

  // 如果提取不到，使用默认
  if (uniqueParts.length === 0) {
    uniqueParts.push('AI', 'technology');
  }

  // 添加场景词提高相关性
  const sceneWords = [];
  const titleLower = title.toLowerCase();
  if (titleLower.includes('deal') || titleLower.includes('contract') || titleLower.includes('签约')) {
    sceneWords.push('meeting', 'signing', 'handshake');
  }
  if (titleLower.includes('launch') || titleLower.includes('announce')) {
    sceneWords.push('event', 'conference', 'stage');
  }
  if (titleLower.includes('robot') || titleLower.includes('agent')) {
    sceneWords.push('robotics', 'automation');
  }
  if (titleLower.includes('chip') || titleLower.includes('GPU')) {
    sceneWords.push('chip', 'processor', 'hardware');
  }

  const finalQuery = [...uniqueParts.slice(0, 3), ...sceneWords.slice(0, 2)].join(' ');

  return {
    chinese: chineseKeywords,
    english: englishWords,
    entities: topEntities,
    query: finalQuery.trim(),
    raw: title
  };
}

/**
 * Level 1: Pexels 搜索
 */
async function searchPexels(query) {
  if (!config.pexels.enabled) return null;

  try {
    const url = `https://api.pexels.com/v1/search?query=${encodeURIComponent(query)}&per_page=${config.pexels.perPage}&orientation=landscape`;
    const res = await fetch(url, {
      headers: { Authorization: config.pexels.apiKey }
    });

    if (res.ok) {
      const data = await res.json();
      if (data.photos && data.photos.length > 0) {
        const photo = data.photos[0];
        return {
          url: photo.src.medium,
          full: photo.src.large2x,
          photographer: photo.photographer,
          source: 'pexels',
          id: photo.id
        };
      }
    }
  } catch (err) {
    console.error('❌ Pexels search failed:', err.message);
  }
  return null;
}

/**
 * Level 2: 默认映射图片
 */
const DEFAULT_IMAGE_MAP = {
  '五角大楼': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80',
  'Pentagon': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80',
  'Defense': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80',
  'Nvidia': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80',
  'AI': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80',
  'robot': 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=900&h=383&fit=crop&q=80',
  'robotics': 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=900&h=383&fit=crop&q=80',
  '智能体': 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=900&h=383&fit=crop&q=80',
  'default': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80'
};

function getDefaultImage(title) {
  const lower = title.toLowerCase();
  for (const [keyword, url] of Object.entries(DEFAULT_IMAGE_MAP)) {
    if (lower.toLowerCase().includes(keyword.toLowerCase())) {
      return url;
    }
  }
  return DEFAULT_IMAGE_MAP.default;
}

/**
 * 主函数
 */
export async function fetchFeaturedImage(title) {
  console.log('\n🎨 Fetching featured image...');
  console.log('   Title:', title.substring(0, 60));

  const keywords = extractKeywords(title);
  console.log('   Query:', keywords.query);

  // Level 1: Pexels
  if (config.pexels.enabled) {
    const result = await searchPexels(keywords.query);
    if (result) {
      console.log('   ✅ Source: Pexels');
      return result;
    }
  } else {
    console.log('   ⚠️  Pexels API key not configured, skipping...');
  }

  // Level 2: Default mapping
  const defaultUrl = getDefaultImage(title);
  console.log('   ⚠️  Using default image');
  return {
    url: defaultUrl,
    source: 'default',
    title: title.substring(0, 30)
  };
}

// CLI test
if (import.meta.url === `file://${process.argv[1]}`) {
  const title = process.argv[2] || 'Pentagon inks deals with Nvidia to deploy AI';
  const result = await fetchFeaturedImage(title);
  console.log('\n📸 Result:', JSON.stringify(result, null, 2));
}
