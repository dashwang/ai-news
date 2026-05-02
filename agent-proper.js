#!/usr/bin/env node
/**
 * AI News Publisher - Proper Agent Skill
 * 作为真正的Agent Skill运行，可以直接使用 agent.llm
 *
 * 使用方式：
 *   openclaw agent run ai-news-publisher --date=2026-05-01 --publish
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, 'data');

// 这个函数会被OpenClaw注入agent上下文后调用
export async function run(agent, args = {}) {
  console.log(`🤖 AI News Publisher (Agent Context)`);
  console.log(`   Model: ${agent?.model?.name || 'unknown'}`);

  const date = args.date || new Date().toISOString().split('T')[0];
  const shouldPublish = args.publish || false;

  console.log(`📚 Loading news for ${date}...`);

  const newsFile = join(dataDir, `news-${date}.json`);
  if (!existsSync(newsFile)) {
    // 尝试昨天
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    const yesterdayFile = join(dataDir, `news-${yesterday}.json`);
    if (existsSync(yesterdayFile)) {
      console.log(`   Using ${yesterday} news`);
      loadAndTranslate(yesterdayFile, agent);
    } else {
      console.error(`❌ No news file found for ${date} or ${yesterday}`);
      console.log('💡 Run fetch first: node fetch_news.js');
      return { error: 'missing-news' };
    }
  } else {
    loadAndTranslate(newsFile, agent);
  }

  async function loadAndTranslate(file, agent) {
    const data = JSON.parse(readFileSync(file, 'utf8'));
    const news = data.news.slice(0, args.limit || 15);
    console.log(`✅ Loaded ${news.length} stories`);

    // Sort by score
    news.sort((a,b) => (b.score||0) - (a.score||0));

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

      if ((i+1) % 3 === 0) console.log(`   Translated ${i+1}/${news.length}`);
    }

    console.log('✅ Translation complete');

    // Save back
    writeFileSync(file, JSON.stringify({ date: date.split('T')[0], news }, null, 2));

    // Generate HTML
    const hl = news[0];
    const html = generateHTML(news, hl, date);
    const htmlFile = join(dataDir, `wechat-html-${date}.html`);
    writeFileSync(htmlFile, html, 'utf8');
    console.log(`📄 HTML: ${htmlFile} (${html.length} chars)`);

    // Publish if requested
    if (shouldPublish) {
      console.log('📤 Publishing to WeChat...');
      // Call publish script (it's standalone)
      const { execSync } = await import('child_process');
      const cmd = `WECHAT_APP_ID="${process.env.WECHAT_APP_ID}" WECHAT_APP_SECRET="${process.env.WECHAT_APP_SECRET}" node ${join(__dirname, 'publish-article.mjs')} "${htmlFile}" "${hl.title_zh}" "${selectImage(hl)}"`;
      try {
        const out = execSync(cmd, { encoding: 'utf8', timeout: 30000 });
        console.log(out);
        const m = out.match(/Draft media_id[:：]\s*(\S+)/);
        if (m) {
          console.log('✅ Draft created:', m[1]);
          return { success: true, draftId: m[1] };
        }
      } catch (e) {
        console.error('❌ Publish error:', e.message);
      }
    }

    return { success: true, count: news.length, headline: hl.title_zh };
  }
}

/**
 * 使用 agent.llm 翻译标题
 */
async function translateTitle(agent, title, source) {
  const prompt = `You are a tech news translator. Translate this English title to Chinese (within 15 characters). Keep it punchy and accurate.

English: "${title}"

Chinese (just the title, no quotes):`;

  try {
    const result = await agent.llm.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
      max_tokens: 50
    });
    let zh = result.content?.trim() || result.text?.trim() || '';
    // Clean
    zh = zh.replace(/^["「『"(.+)["」』"]$/, '$1');
    return zh.length > 2 ? zh : simpleTitleTranslate(title);
  } catch (e) {
    console.error('  ⚠️ LLM translate failed:', e.message);
    return simpleTitleTranslate(title);
  }
}

/**
 * 使用 agent.llm 生成摘要
 */
async function translateSummary(agent, title, titleZh, source) {
  const prompt = `Write a 120-150 Chinese summary for this tech news.

English title: ${title}
Chinese title: ${titleZh}
Source: ${source}

Requirements:
- Accurate core points
- Natural Chinese
- No "本文报道" opening
- Just the summary text:`;

  try {
    const result = await agent.llm.chat({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.4,
      max_tokens: 300
    });
    let summary = result.content?.trim() || result.text?.trim() || '';
    summary = summary.replace(/^["「『"(.+)["」』"]$/s, '$1');
    return summary.length > 20 ? summary : simpleSummary(titleZh, source);
  } catch (e) {
    console.error('  ⚠️ LLM summary failed:', e.message);
    return simpleSummary(titleZh, source);
  }
}

/**
 * 生成HTML
 */




function generateHTML(news, hl, date) {
  // 计算各板块，每个最多取5条（按score排序）
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

  function fmtSection(name, items) {
    if (!items.length) return '';
    const color = colors[name];
    const rows = items.map((n, idx) => {
      let summary = (n.summary_zh || '');
      const title = n.title_zh || n.title || '';
      if (summary.startsWith(title)) {
        summary = summary.substring(title.length).trim();
      }
      summary = summary.replace(/^[:：\s]+/, '');
      if (summary.length < 120) {
        summary = summary + '。本文涵盖AI领域重要动态，涉及技术突破、产业动向、政策法规等多个方面，值得关注。';
      }
      summary = summary.substring(0, 140).trim();

      return '<div style="padding:16px 0;border-bottom:1px solid #f0f0f0;line-height:1.55"><div style="font-size:15px;font-weight:700;margin-bottom:6px;color:#111">' +
        idx + '. <a href="' + n.url + '" style="color:#1976d2;text-decoration:none">' + title + '</a></div>' +
        '<div style="font-size:13px;color:#555;line-height:1.6">' + summary + '</div></div>';
    }).join('');

    return '<div style="margin:12px 0"><h3 style="font-size:17px;font-weight:800;color:' + color + ';margin:0 0 8px;padding-bottom:4px;border-bottom:2px solid ' + color + '">' + name + '</h3>' + rows + '</div>';
  }

  const body = Object.entries(sections).map(([n, i]) => fmtSection(n, i)).filter(Boolean).join('');
  const cleanBody = body.replace(/\n/g, '');

  const dynamicTitle = hl.title_zh || hl.title || 'AI News';

  return '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>' + dynamicTitle + '</title>' +
    '<style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;font-size:15px;line-height:1.55;color:#333;margin:0;padding:10px;background:#fff}a{color:#1976d2;text-decoration:none}img{max-width:100%;border-radius:4px}</style></head><body>' + cleanBody + '</body></html>';
}






function selectImage(item) {

function selectImage(item) {
  const t = (item.title_zh || item.title || '').toLowerCase();
  if (t.includes('robot') || t.includes('agent') || t.includes('智能体')) {
    return 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=900&h=383&fit=crop&q=80';
  }
  return 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80';
}

function simpleTitleTranslate(title) {
  const d = {
    'AI': 'AI', 'LLM': '大语言模型', 'Google': '谷歌', 'Microsoft': '微软',
    'Meta': 'Meta', 'Nvidia': '英伟达', 'Pentagon': '五角大楼',
    'robot': '机器人', 'humanoid': '人形', 'acquisition': '收购',
    'Musk v. Altman': '马斯克诉阿尔特曼', 'ChatGPT': 'ChatGPT',
    'Ask HN:': 'Ask HN：', 'Show HN:': 'Show HN：'
  };
  let zh = title;
  for (const [k, v] of Object.entries(d)) zh = zh.replace(new RegExp(k, 'g'), v);
  return zh;
}

function simpleSummary(titleZh, source) {
  return `本文报道了「${titleZh}」，来自${source}。该新闻涉及AI领域最新动态，值得关注。`;
}

// 如果直接运行（而非通过openclaw agent），则模拟agent上下文
if (import.meta.url === `file://${process.argv[1]}`) {
  // 作为独立脚本运行（兼容旧模式）
  const args = {};
  for (let i = 2; i < process.argv.length; i++) {
    const arg = process.argv[i];
    if (arg === '--publish') args.publish = true;
    if (arg.startsWith('--date=')) args.date = arg.slice(7);
    if (arg.startsWith('--limit=')) args.limit = parseInt(arg.slice(8));
  }

  // 创建模拟agent（使用kilo CLI fallback）
  const mockAgent = {
    model: { name: 'kilo-fallback' },
    llm: {
      chat: async ({ messages }) => {
        const prompt = messages[0]?.content || '';
        try {
          const result = execSync(`echo "${prompt.substring(0, 200)}" | kilo`, {
            encoding: 'utf8', timeout: 20000, stdio: ['pipe','pipe','pipe']
          });
          return { content: result.trim() };
        } catch(e) {
          return { content: simpleTitleTranslate(prompt) };
        }
      }
    }
  };

  run(mockAgent, args).then(() => process.exit(0)).catch(e => {
    console.error(e);
    process.exit(1);
  });
}
