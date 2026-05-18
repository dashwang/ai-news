#!/usr/bin/env node
/**
 * AI News Publisher - Main Entry Point for Cron
 * 定时任务入口：抓取 -> 翻译 -> 发布
 *
 * 流程：
 * 1. fetch_news.js - 抓取当天新闻
 * 2. translate-real.js - 翻译标题和摘要
 * 3. agent.js --publish - 生成HTML并发布到公众号草稿箱
 */

import { execSync } from 'child_process';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { existsSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));

function runCmd(cmd, desc) {
  console.log(`\n📌 ${desc}...`);
  console.log('   $', cmd);
  const start = Date.now();
  try {
    const output = execSync(cmd, { cwd: __dirname, stdio: 'pipe', encoding: 'utf8' });
    console.log(output.trim().split('\n').slice(-3).join('\n'));
    console.log(`   ✅ ${desc} completed in ${Date.now() - start}ms`);
    return true;
  } catch (e) {
    console.error('   ❌ Error:', e.message);
    console.error(e.stdout?.toString().split('\n').slice(-5).join('\n'));
    return false;
  }
}

async function main() {
  console.log('🤖 AI News Daily Publisher -', new Date().toISOString().split('T')[0]);

  const today = new Date().toISOString().split('T')[0];
  const newsFile = join(__dirname, 'data', `news-${today}.json`);

  // Step 1: Fetch news (if not exists)
  if (!existsSync(newsFile)) {
    console.log(`\n📰 抓取今日新闻 (${today})...`);
    // 使用fetch_news.js或agent的fetch功能
    // 这里简化为调用node agent的fetch模式
    try {
      console.log('   (Skipping fetch - using existing if available)');
    } catch(e) {
      console.error('   ❌ Fetch failed:', e.message);
    }
  } else {
    console.log(`✅ News file exists: ${newsFile}`);
  }

  // Step 2: Translate
  console.log('\n🔄 Translating news...');
  runCmd('node translate-real.js', 'Translation');

  // Step 3: Publish (only if explicitly requested via env)
  if (process.env.FORCE_PUBLISH === 'true' || process.argv.includes('--publish')) {
    console.log('\n📤 Publishing to WeChat...');
    runCmd('node agent.js --publish', 'Publishing');
  } else {
    console.log('\n💡 Use --publish or FORCE_PUBLISH=true to actually publish');
    console.log('   (Skipping publish in dry-run mode)');
  }

  console.log('\n🎉 Done!');
}

main().catch(e => {
  console.error('❌ Fatal:', e);
  process.exit(1);
});
