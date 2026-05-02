/**
 * Test script for fetch-featured-image.js
 * 在没有 API key 时测试回退逻辑
 */

// 模拟环境变量（无 API key）
process.env.WECHAT_PEXELS_API_KEY = '';
process.env.WECHAT_GOOGLE_CSE_ID = '';
process.env.WECHAT_GOOGLE_API_KEY = '';

// 导入测试
import { fetchFeaturedImage } from './fetch-featured-image.js';

console.log('🧪 Testing image fetcher (no API keys)...\n');

const testTitles = [
  'Pentagon inks deals with Nvidia, Microsoft, and AWS to deploy AI on classified networks',
  'Meta buys robotics startup to bolster its humanoid AI ambitions',
  'AI推理成本迎来拐点：效率突破将重塑行业格局',
  'Musk v. Altman is just getting started'
];

for (const title of testTitles) {
  console.log(`\n📰 Testing: "${title.substring(0, 50)}..."`);
  try {
    const result = await fetchFeaturedImage(title);
    console.log(`   🖼️  Image URL: ${result.url.substring(0, 80)}...`);
    console.log(`   📦 Source: ${result.source}`);
  } catch (err) {
    console.error(`   ❌ Error: ${err.message}`);
  }
}

console.log('\n✅ Test complete!');
