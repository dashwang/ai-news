#!/usr/bin/env node
/**
 * AI News Publisher - Agent Skill (Publish Only) - V5
 * Fixed: removed item borders (cleaner look)
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import https from 'https';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, 'data');
mkdirSync(dataDir, { recursive: true });

const CONFIG = {
  wechatAppId: process.env.WECHAT_APP_ID || '',
  wechatAppSecret: process.env.WECHAT_APP_SECRET || '',
};

function selectImage(item) {
  const t = (item.title||'').toLowerCase();
  if (t.includes('deepseek') || t.includes('model') || t.includes('llm')) {
    return 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80';
  }
  if (t.includes('robot') || t.includes('agent')) {
    return 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=900&h=383&fit=crop&q=80';
  }
  return 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80';
}

function generateWechatHTML(news, hl) {
  const sections = {
    'Hacker News': news.filter(n=>n.source==='HackerNews'),
    'TechCrunch AI': news.filter(n=>n.source==='TechCrunch'),
    'Latent Space': news.filter(n=>n.source==='LatentSpace'),
    'Substack': news.filter(n=>n.source==='Substack'),
  };
  const colors = {
    'Hacker News': '#ff6b35',
    'TechCrunch AI': '#1a73e8',
    'Latent Space': '#9c27b0',
    'Substack': '#0f9d58',
  };

  const fmt = (name, items) => {
    if (!items.length) return '';
    const color = colors[name] || '#333';
    return `<div style="margin:1px 0"><h3 style="font-size:14px;font-weight:800;margin:0 0 3px;color:${color};border-left:3px solid ${color};padding-left:8px">${name}</h3>${items.map((n) => `
      <div style="margin-bottom:1px">
        <div style="font-size:15px;font-weight:700;line-height:1.4;color:#111;margin-bottom:0">
          ${n.title_zh || n.title}
        </div>
        <div style="font-size:13px;color:#444;line-height:1.75;margin-top:1px">
          ${(n.summary_zh || '').substring(0, 300)}
        </div>
      </div>
    `).join('')}</div>`;
  };

  const body = Object.entries(sections).map(([n,i])=>fmt(n,i)).filter(Boolean).join('\n');
  const img = selectImage(hl);
  const date = new Date().toISOString().split('T')[0];
  const hlText = (hl.title_zh || hl.title);

  return `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>北美AI圈日报 ${date}</title><style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;line-height:1.6;color:#333;margin:0;padding:0;background:#fff}.header{text-align:center;padding:6px 2px 2px;border-bottom:1px solid #e65100;margin-bottom:2px}.headline{font-size:16px;font-weight:800;color:#111;margin:2px 0 4px;line-height:1.4}.headline-img{width:100%;max-width:600px;height:auto;border-radius:8px;margin:0 auto 3px;display:block}.section{margin:1px 0}</style></head><body><div class="header"><div class="headline">${hlText}</div><img src="${img}" class="headline-img" alt="头条配图"></div>
${body}</body></html>`;
}

function loadNews(date) {
  const jsonFile = join(dataDir, `news-${date}.json`);
  if (!existsSync(jsonFile)) {
    throw new Error(`News file not found: ${jsonFile}. Run fetch first, then translate.`);
  }
  const data = JSON.parse(readFileSync(jsonFile, 'utf8'));
  if (!data.news || !Array.isArray(data.news)) {
    throw new Error('Invalid news file format');
  }
  for (const n of data.news) {
    if (!n.title_zh) n.title_zh = n.title;
    if (!n.summary_zh) n.summary_zh = n.summary?.substring(0,300) || '';
  }
  return data.news;
}

function selectHeadline(news) {
  return [...news].sort((a,b) => (b.score||0) - (a.score||0) || 0)[0];
}

function checkDuplicated(date) {
  const f = join(dataDir, 'published.json');
  if (existsSync(f)) {
    try {
      const d = JSON.parse(readFileSync(f, 'utf8'));
      const list = d.published || Object.values(d);
      if (list.find(item => item.date === date)) {
        console.log(`⚠️ ${date} 已发布`);
        return true;
      }
    } catch(e){}
  }
  return false;
}

function recordPublished(info) {
  const f = join(dataDir, 'published.json');
  let d = {};
  if (existsSync(f)) d = JSON.parse(readFileSync(f, 'utf8'));
  if (!d.published) d.published = [];
  d.published.push({ date: new Date().toISOString().split('T')[0], ...info });
  writeFileSync(f, JSON.stringify(d, null, 2));
  console.log('📝 记录完成');
}

async function publishToWechat(html, title) {
  if (!CONFIG.wechatAppId || !CONFIG.wechatAppSecret) {
    console.log('⚠️ WECHAT_* not set, skipping publish');
    return { draftId: 'missing-config' };
  }
  const tmp = join(dataDir, `tmp-${Date.now()}.html`);
  writeFileSync(tmp, html, 'utf8');
  try {
    const { execSync } = await import('node:child_process');
    const cmd = `cd ${__dirname} && WECHAT_APP_ID="${CONFIG.wechatAppId}" WECHAT_APP_SECRET="${CONFIG.wechatAppSecret}" node publish-article.mjs "${tmp}" "${title}" "${selectImage({title})}"`;
    const out = execSync(cmd, { encoding: 'utf8', stdio: ['pipe','pipe','pipe'], timeout: 30000 });
    console.log(out);
    const m = out.match(/Draft media_id[:：]\s*(\S+)/);
    if (m) {
      console.log('✅ Published, media_id:', m[1]);
      return { draftId: m[1] };
    }
    return { draftId: 'ok' };
  } catch (e) {
    console.error('❌ Publish failed:', e.message);
    return { draftId: 'error' };
  }
}

async function run(args = {}) {
  console.log(`🤖 AI News Agent - Publish Only (${new Date().toISOString()})`);
  const shouldPublish = args.publish || false;
  const date = args.date || new Date().toISOString().split('T')[0];

  console.log(`📚 Loading news for ${date}...`);
  let news = loadNews(date);
  console.log(`✅ Loaded ${news.length} stories`);

  news.sort((a,b) => (b.score||0) - (a.score||0));
  const limit = args.limit || 15;
  news = news.slice(0, limit);
  console.log(`📊 Top ${news.length} selected`);

  const hl = selectHeadline(news);
  console.log('📰 Headline:', hl.title_zh || hl.title);

  const html = generateWechatHTML(news, hl);
  const htmlFile = join(dataDir, `wechat-html-${date}.html`);
  writeFileSync(htmlFile, html, 'utf8');
  console.log(`✅ HTML: ${htmlFile} (${html.length} chars)`);
  // Archive a timestamped copy for version history
  const archiveFile = join(dataDir, `wechat-html-${date}-v${Date.now()}.html`);
  writeFileSync(archiveFile, html, 'utf8');
  console.log(`📦 Archived: ${archiveFile}`);

  if (shouldPublish) {
    if (checkDuplicated(date)) {
      console.log('⚠️ Already published today');
    } else {
      const res = await publishToWechat(html, `北美AI圈日报 ${date}`);
      recordPublished({ title: hl.title_zh || hl.title, draftId: res.draftId, count: news.length });
    }
  } else {
    console.log('💡 Use --publish to create draft');
  }

  console.log('🎉 Done');
  return { success: true, count: news.length, headline: hl.title_zh };
}

if (process.argv[1] && process.argv[1].includes('agent.js')) {
  const args = {};
  for (let i = 2; i < process.argv.length; i++) {
    const arg = process.argv[i];
    if (arg === '--publish') args.publish = true;
    if (arg.startsWith('--date=')) args.date = arg.slice(7);
    if (arg.startsWith('--limit=')) args.limit = parseInt(arg.slice(8), 10);
  }
  run(args).then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
}

export { run };
