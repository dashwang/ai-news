#!/usr/bin/env node
// Build WeChat HTML 2026-05-18 — from news JSON (Chinese titles already set)
import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, 'data');
const newsFile  = join(dataDir, 'news-2026-05-18.json');
const htmlFile  = join(dataDir, 'wechat-html-2026-05-18.html');

const { news: allNews } = JSON.parse(readFileSync(newsFile, 'utf8'));
const DATE = '2026-05-18';

console.log('📄 Building WeChat HTML...');

const sorted = allNews.sort((a,b) => (b.score||0) - (a.score||0));
const top = sorted.slice(0, 15);

// Simple majority-zh check
const cnCount = top.filter(n => (n.title_zh||'') !== n.title).length;
console.log(`📊 Chinese titles: ${cnCount}/15`);

const hlTitle = top[0].title_zh || top[0].title;

const sectionsCfg = [
  { name:'TechCrunch AI',   color:'#1a73e8',
    items: top.filter(n => n.source === 'TechCrunch') },
  { name:'Hacker News',     color:'#ff6b35',
    items: top.filter(n => n.source === 'HackerNews') },
  { name:'Substack',        color:'#9c27b8',
    items: top.filter(n => ['LatentSpace','TheDecoder','MITTechReview'].includes(n.source)) },
];

function sectionHTML(c) {
  const items = c.items;
  if (!items.length) return '';
  const rows = items.map((n,i) => {
    let t = n.title_zh || n.title;
    let s = n.summary_zh || t;
    s = s.replace(/\s+/g,' ').trim().substring(0, 160);
    if (!s) s = t;

    const hot = (n.source==='HackerNews' && n.score>=2)
      ? '<span style="display:inline-block;background:#ff6b35;color:#fff;font-size:10px;padding:1px 5px;border-radius:3px;margin-left:6px;font-weight:400">🔥 热门</span>'
      : '';

    return `      <div style="padding:18px 0 ${i<items.length-1?'10px':'0'};border-bottom:1px solid #f5f5f5">
        <div style="font-size:15px;font-weight:700;color:#111;line-height:1.55;margin-bottom:6px">${i+1}. ${t}${hot}</div>
        <div style="font-size:13.5px;color:#666;line-height:1.7">${s}</div>
      </div>`;
  }).join('\n');
  return `    <div style="margin:30px 0 0">
      <h3 style="font-size:19px;font-weight:800;color:${c.color};margin:0 0 14px;padding-bottom:6px;border-bottom:2px solid ${c.color}">${c.name}</h3>
      <div style="padding:0 2px">\n${rows}\n      </div>
    </div>`;
}

const secHTML = sectionsCfg.map(c => sectionHTML(c)).filter(Boolean).join('\n');
const total = sectionsCfg.reduce((s,c) => s + c.items.length, 0);

const html = `<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AI 日报 · ${DATE}</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;line-height:1.6;color:#333;margin:0;padding:0;background:#fff}</style>
</head><body>

<div style="text-align:center;padding:32px 16px 24px;border-bottom:3px solid #e65100">
  <div style="font-size:23px;font-weight:800;color:#111;line-height:1.4;margin-bottom:10px">${hlTitle}</div>
  <div style="font-size:13px;color:#888">${DATE} · 今日 ${total} 条精选</div>
</div>

${secHTML}

<div style="text-align:center;padding:32px 0 48px;color:#aaa;font-size:12px;border-top:1px solid #eee;margin-top:36px">
  <p style="margin:0 0 6px;letter-spacing:.5px">数据来源：Hacker News · TechCrunch · Latent Space · The Decoder · MIT Tech Review</p>
  <p style="margin:0">由 AI News Publisher · 每日自动生成</p>
</div>

</body></html>`;

writeFileSync(htmlFile, html, 'utf8');
console.log(`✅ HTML: ${htmlFile}  (${html.length} chars)`);
console.log(`📌 Headline: ${hlTitle}`);
