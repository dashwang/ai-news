#!/usr/bin/env node
/**
 * Generate WeChat HTML (2026-05-15) - 7 sections with full translations
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, 'data');
const newsFile = join(dataDir, 'news-2026-05-15.json');
const htmlFile = join(dataDir, 'wechat-html-2026-05-15.html');

const { news } = JSON.parse(readFileSync(newsFile, 'utf8'));
const date = '2026-05-15';

console.log('📄 Generating WeChat HTML with translations...');

// Sort by score descending, take all 20
const sorted = news.sort((a, b) => (b.score || 0) - (a.score || 0));
const top = sorted.slice(0, 20);
const hl = top[0];

// Group into 5 sections
const sections = {
  '🔥 Hacker News': top.filter(n => n.source === 'HackerNews').slice(0, 5),
  '📰 TechCrunch': top.filter(n => n.source === 'TechCrunch').slice(0, 5),
  '🎙️ Latent Space': top.filter(n => n.source === 'LatentSpace').slice(0, 5),
  '💡 MIT Tech Review': top.filter(n => n.source === 'MITTechReview').slice(0, 5),
};

console.log('📊 Section counts:');
Object.entries(sections).forEach(([k, v]) => console.log(`   ${k}: ${v.length} items`));

// Section colors (wechat-html-v5 inspired, compact)
const colors = {
  '🔥 Hacker News': '#ff6b35',
  '📰 TechCrunch': '#1a73e8',
  '🎙️ Latent Space': '#9c27b0',
  '💡 MIT Tech Review': '#d32f2f',
};

function smartTruncate(text, maxLen) {
  if (text.length <= maxLen) return text;
  const cut = text.substring(0, maxLen);
  const puncts = ['。', '？', '！', '；', '，', '.', '!', '?', ';'];
  let bestPos = -1;
  for (const p of puncts) {
    const pos = cut.lastIndexOf(p);
    if (pos > 100 && pos > bestPos) bestPos = pos;
  }
  if (bestPos !== -1) return text.substring(0, bestPos + 1);
  const space = cut.lastIndexOf(' ');
  if (space > 100) return text.substring(0, space);
  return text.substring(0, maxLen);
}

function sectionHTML(name, items) {
  if (!items.length) return '';
  const icon = name.split(' ')[0];
  const label = name.split(' ').slice(1).join(' ');
  const color = colors[name];
  const rows = items.map((n, i) => {
    const title = n.title_zh || n.title || '';
    let summary = (n.summary_zh || '').trim();
    // Strip title prefix if embedded
    if (summary.startsWith(title)) summary = summary.substring(title.length).trim();
    summary = summary.replace(/^[:：\s]+/, '').trim();
    // Ensure ~200 chars
    if (summary.length > 200) summary = smartTruncate(summary, 200);
    if (summary.length < 120 && i < items.length - 1) summary += '。';

    return `      <div style="padding:16px 0;border-bottom:1px solid #f5f5f5;line-height:1.6">
        <div style="font-size:16px;font-weight:700;color:#111;margin-bottom:6px">
          <a href="${n.url}" style="color:#1976d2;text-decoration:none">${i + 1}. ${title}</a>
        </div>
        <div style="font-size:14px;color:#555;line-height:1.65">${summary}</div>
      </div>`;
  }).join('');

  return `    <div style="margin:24px 0 0;">
      <h3 style="font-size:18px;font-weight:800;color:${color};margin:0 0 12px;padding-bottom:6px;border-bottom:2px solid ${color};display:flex;align-items:center;gap:8px">
        <span style="font-size:19px">${icon}</span> ${label}
      </h3>
      <div style="padding:0 4px">
${rows}
      </div>
    </div>`;
}

const body = Object.entries(sections).map(([name, items]) => sectionHTML(name, items)).filter(Boolean).join('\n');
const hlTitle = hl.title_zh || hl.title || 'AI News Daily';

const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>北美AI圈日报 ${date}</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;font-size:15px;line-height:1.6;color:#333;margin:0;padding:0;background:#fff;-webkit-font-smoothing:antialiased}a{color:#1976d2;text-decoration:none}a:hover{color:#0d47a1}
.header{text-align:center;padding:36px 20px 28px;background:linear-gradient(135deg,#fafbfc 0%,#e8eaf6 100%);border-bottom:1px solid #e0e0e0;margin-bottom:12px}
.headline{font-size:26px;font-weight:800;color:#111;margin:12px 0 10px;line-height:1.35}.meta{font-size:13px;color:#777;letter-spacing:0.3px}.section{max-width:680px;margin:0 auto;padding:0 16px}.footer{text-align:center;padding:24px 0 40px;color:#999;font-size:12px;border-top:1px solid #eee;margin-top:20px}h3{margin:0}@media(max-width:480px){.headline{font-size:22px}}
</style></head>
<body>
  <div class="header">
    <div class="headline">${hlTitle}</div>
    <div class="meta">${date} · 今日${top.length}条 · 5大来源</div>
  </div>

  <div class="section">
${body}
  </div>

  <div class="footer">
    <p>数据来源：Hacker News · TechCrunch · Latent Space · MIT Technology Review</p>
    <p style="margin-top:10px">由 AI News Publisher 自动生成</p>
  </div>
</body></html>`;

writeFileSync(htmlFile, html, 'utf8');
console.log(`✅ HTML generated: ${htmlFile}`);
console.log(`📊 Size: ${html.length} chars`);

// Quick verification
console.log(`\n📋 Verification:`);
let totalItems = 0;
Object.entries(sections).forEach(([name, items]) => {
  console.log(`   ${name}: ${items.length} items`);
  totalItems += items.length;
});
console.log(`   Total: ${totalItems} items`);
console.log(`\n📌 Headline: ${hlTitle}`);
