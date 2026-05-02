#!/usr/bin/env node
/**
 * AI News Publisher - Native Agent Skill (V3 - Fixed)
 *
 * Properly uses agent.llm and agent.tools for publishing
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { fetchFeaturedImage } from './fetch-featured-image.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, 'data');
mkdirSync(dataDir, { recursive: true });

/**
 * Main entry point
 */
export async function run(agent, args = {}) {
  console.log(`🤖 AI News Publisher (Native Agent Skill)`);
  console.log(`   Model: ${agent?.model?.name || 'unknown'}`);

  const date = args.date || new Date().toISOString().split('T')[0];
  const shouldPublish = args.publish || false;
  const limit = args.limit || 15;

  console.log(`📅 Date: ${date}`);
  console.log(`📊 Limit: ${limit}`);

  // Step 1: Ensure news exists
  const newsFile = join(dataDir, `news-${date}.json`);
  if (!existsSync(newsFile)) {
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    const yesterdayFile = join(dataDir, `news-${yesterday}.json`);
    if (existsSync(yesterdayFile)) {
      console.log(`📰 Using yesterday's news (${yesterday})`);
      await processNews(yesterdayFile, agent, limit, shouldPublish, date);
    } else {
      console.error(`❌ No news file found for ${date} or ${yesterday}`);
      console.log('💡 Fetch first: node fetch_news.js');
      return { error: 'no-news' };
    }
  } else {
    await processNews(newsFile, agent, limit, shouldPublish, date);
  }
}

/**
 * Process news file: translate, generate HTML, optionally publish
 */
async function processNews(newsFile, agent, limit, shouldPublish, date) {
  const { news: allNews } = JSON.parse(readFileSync(newsFile, 'utf8'));
  console.log(`✅ Loaded ${allNews.length} raw stories`);

  // Sort and limit
  const sorted = allNews.sort((a, b) => (b.score || 0) - (a.score || 0));
  const news = sorted.slice(0, limit);
  console.log(`📊 Selected top ${news.length}`);

  // Translate using agent.llm
  console.log('🔄 Translating with agent.llm...');
  for (let i = 0; i < news.length; i++) {
    const item = news[i];

    if (!item.title_zh || item.title_zh === item.title) {
      item.title_zh = await translateTitle(agent, item.title, item.source);
    }

    if (!item.summary_zh || item.summary_zh.length < 30) {
      item.summary_zh = await translateSummary(agent, item.title, item.title_zh, item.source);
    }

    if ((i + 1) % 3 === 0) console.log(`   Translated ${i + 1}/${news.length}`);
  }

  console.log('✅ Translation complete');

  // Save translated news
  writeFileSync(newsFile, JSON.stringify({ date, news: allNews }, null, 2));

  // Show preview
  console.log('\n📝 Preview (first 3):');
  news.slice(0, 3).forEach((n, idx) => {
    console.log(`\n[${idx + 1}] ${n.title}`);
    console.log(`    → ${n.title_zh}`);
    console.log(`    📝 ${n.summary_zh.substring(0, 80)}...`);
  });

  // Generate HTML
  const hl = news[0];
  const html = generateHTML(news, hl, date);
  const htmlFile = join(dataDir, `wechat-html-${date}.html`);
  writeFileSync(htmlFile, html, 'utf8');
  console.log(`\n📄 HTML: ${htmlFile} (${html.length} chars)`);

  // Publish if requested
  if (shouldPublish) {
    return await publish(agent, news, hl, date, htmlFile);
  }

  return { success: true, count: news.length, headline: hl.title_zh };
}

/**
 * Translate title using agent.llm
 */
async function translateTitle(agent, title, source) {
  const prompt = `你是一位专业的科技新闻翻译。请将以下英文标题翻译成简洁有力的中文标题（不超过15字）。

英文标题："${title}"
来源：${source}

要求：
- 准确传达核心信息
- 符合中文新闻标题风格
- 简洁有力
- 只输出中文标题，不要任何解释

直接输出：`;

  try {
    const result = await agent.llm.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
      max_tokens: 50
    });

    let zh = (result.content || result.text || '').trim();
    // Remove quotes and prefixes
    zh = zh.replace(/^["『「]|[》」']$/g, '').trim();
    zh = zh.split('\n')[0].trim();

    if (zh.length > 2 && zh.length < 50) {
      console.log(`  ✓ "${title.substring(0, 30)}" → "${zh}"`);
      return zh;
    }
  } catch (e) {
    console.error('  ⚠️ LLM error:', e.message);
  }

  return fallbackTitle(title);
}

/**
 * Translate summary using agent.llm
 */
async function translateSummary(agent, title, titleZh, source) {
  const prompt = `请为以下科技新闻生成一段120-150字的中文摘要。

英文标题：${title}
中文标题：${titleZh}
来源：${source}

要求：
1. 准确概括新闻核心内容
2. 语言自然流畅，符合中文新闻风格
3. 不要以"本文报道"或"据悉"开头
4. 直接输出摘要内容，不要前缀

摘要：`;

  try {
    const result = await agent.llm.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.4,
      max_tokens: 300
    });

    let summary = (result.content || result.text || '').trim();
    summary = summary.replace(/^["『「]|[》』"]$/g, '').trim();
    summary = summary.split('\n').filter(l => l.trim().length > 0)[0] || summary;

    if (summary.length > 50) {
      console.log(`  ✓ Summary: ${summary.substring(0, 50)}...`);
      return summary;
    }
  } catch (e) {
    console.error('  ⚠️ LLM error:', e.message);
  }

  return fallbackSummary(titleZh, source);
}

/**
 * Fallback title translation
 */
function fallbackTitle(title) {
  const dict = {
    'AI': 'AI', 'LLM': '大语言模型', 'OpenAI': 'OpenAI',
    'Google': '谷歌', 'Microsoft': '微软', 'Amazon': '亚马逊', 'Meta': 'Meta',
    'Nvidia': '英伟达', 'Pentagon': '五角大楼', 'NSA': 'NSA',
    'robot': '机器人', 'humanoid': '人形', 'agent': '智能体', 'robotics': '机器人技术',
    'acquisition': '收购', 'acquire': '收购', 'buyout': '收购',
    'Musk v. Altman': '马斯克诉阿尔特曼', 'Elon Musk': '马斯克',
    'ChatGPT': 'ChatGPT', 'GPT': 'GPT',
    'Ask HN:': 'Ask HN：', 'Show HN:': 'Show HN：',
    '[AINews]': '[AINews]',
    'TechCrunch': 'TechCrunch', 'Hacker News': 'Hacker News',
    'MIT Tech Review': 'MIT Tech Review'
  };

  let zh = title;
  for (const [en, cn] of Object.entries(dict)) {
    zh = zh.replace(new RegExp(en, 'gi'), cn);
  }
  return zh.replace(/\s+/g, ' ').trim();
}

/**
 * Fallback summary
 */
function fallbackSummary(titleZh, source) {
  const srcMap = {
    'HackerNews': 'Hacker News技术社区',
    'TechCrunch': 'TechCrunch科技媒体',
    'LatentSpace': 'Latent SpaceAI媒体',
    'TheDecoder': 'TheDecoder科技媒体',
    'MITTechReview': 'MIT Technology Review'
  };
  const srcName = srcMap[source] || source;
  return `关于「${titleZh}」的报道。${srcName}发布了这一消息，涉及AI领域的重要动态。`;
}

/**
 * Generate WeChat HTML
 */







function generateHTML(news, hl, date) {
  const techCrunch = news.filter(n => n.source === 'TechCrunch').sort((a,b) => (b.score||0) - (a.score||0)).slice(0, 5);
  const hackerNews = news.filter(n => n.source === 'HackerNews').sort((a,b) => (b.score||0) - (a.score||0)).slice(0, 5);
  const substack = news.filter(n => n.source === 'LatentSpace' || n.source === 'TheDecoder' || n.source === 'MITTechReview')
    .sort((a,b) => (b.score||0) - (a.score||0)).slice(0, 5);

  const sections = {
    'TechCrunch AI': techCrunch,
    'Hacker News': hackerNews,
    'Substack': substack
  };

  const colors = {
    'TechCrunch AI': '#1a73e8',
    'Hacker News': '#ff6b35',
    'Substack': '#9c27b0'
  };

  function smartTruncate(text, minLen, maxLen) {
    if (text.length <= maxLen) return text;
    const cut = text.substring(0, maxLen);
    const puncts = ['。', '？', '！', '；', '，'];
    let bestPos = -1;
    for (const p of puncts) {
      const pos = cut.lastIndexOf(p);
      if (pos > minLen && pos > bestPos) bestPos = pos;
    }
    if (bestPos !== -1) return text.substring(0, bestPos + 1);
    return text.substring(0, maxLen);
  }

  function fmtSection(name, items) {
    if (!items.length) return '';
    const color = colors[name];
    const rows = items.map((n, idx) => {
      let summary = (n.summary_zh || '');
      const title = n.title_zh || n.title || '';
      if (summary.startsWith(title)) summary = summary.substring(title.length).trim();
      summary = summary.replace(/^[:：\s]+/, '');

      if (summary.length > 105) {
        summary = smartTruncate(summary, 100, 105);
      } else if (summary.length < 100) {
        if (!summary.endsWith('。')) summary += '。';
      }
      summary = summary.trim();

      return '<div style="padding:20px 0;border-bottom:1px solid #f0f0f0;line-height:1.55"><div style="font-size:15px;font-weight:700;margin-bottom:8px;color:#111">' +
        (idx + 1) + '. <a href="' + n.url + '" style="color:#1976d2;text-decoration:none">' + title + '</a></div>' +
        '<div style="font-size:13px;color:#555;line-height:1.6">' + summary + '</div></div>';
    }).join('');

    return '<div style="margin:16px 0"><h3 style="font-size:17px;font-weight:800;color:' + color + ';margin:0 0 10px;padding-bottom:4px;border-bottom:2px solid ' + color + '">' + name + '</h3>' + rows + '</div>';
  }

  const body = Object.entries(sections).map(([name, items]) => fmtSection(name, items)).filter(Boolean).join('');
  const cleanBody = body.replace(/\n/g, '');
  const dynamicTitle = hl.title_zh || hl.title || 'AI News';

  return '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>' + dynamicTitle + '</title>' +
    '<style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;font-size:15px;line-height:1.55;color:#333;margin:0;padding:10px;background:#fff}a{color:#1976d2;text-decoration:none}img{max-width:100%;border-radius:4px}</style></head><body>' + cleanBody + '</body></html>';
}









/**
 * Select cover image using Pexels search with fallback
 */
async function selectImage(hl) {
  const title = hl.title_zh || hl.title || 'AI News';

  try {
    // 尝试获取动态配图
    const imageInfo = await fetchFeaturedImage(title);
    return imageInfo.url;
  } catch (err) {
    console.error('❌ Image fetch failed:', err.message);
    // 回退到基于规则的简单选择
    const t = title.toLowerCase();
    if (t.includes('robot') || t.includes('agent') || t.includes('智能体') || t.includes('robotics')) {
      return 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=900&h=383&fit=crop&q=80';
    }
    return 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80';
  }
}

/**
 * Publish to WeChat using agent tool
 * Called when --publish flag is set
 */
async function publish(agent, news, hl, date, htmlFile) {
  console.log('📤 Publishing to WeChat...');

  // Method 1: Use agent tool if available (preferred)
  if (agent?.tools?.publishWechat) {
    try {
      const result = await agent.tools.publishWechat({
        htmlFile,
        title: hl.title_zh,
        coverUrl: await selectImage(hl)
      });
      console.log('✅ Published via agent tool:', result.draftId);
      return result;
    } catch (e) {
      console.error('  ⚠️ Tool publish failed:', e.message);
    }
  }

  // Method 2: Fallback to child_process
  console.log('   Using child_process fallback...');
  const cmd = `WECHAT_APP_ID="${process.env.WECHAT_APP_ID}" WECHAT_APP_SECRET="${process.env.WECHAT_APP_SECRET}" node ${join(__dirname, 'publish-article.mjs')} "${htmlFile}" "${hl.title_zh}" ${await selectImage(hl)}`;

  try {
    const out = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
    const m = out.match(/Draft media_id[:：]\s*(\S+)/);
    if (m) {
      console.log('✅ Draft created:', m[1]);
      return { success: true, draftId: m[1], count: news.length, headline: hl.title_zh };
    }
  } catch (e) {
    console.error('❌ Publish error:', e.message);
    return { success: false, error: e.message };
  }
}

// Standalone mode (not used in production)
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log('⚠️  This skill should be run via: openclaw agent run ai-news-publisher');
  console.log('   Not as standalone node script.');
  process.exit(1);
}
