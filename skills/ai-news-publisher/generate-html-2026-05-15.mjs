#!/usr/bin/env node
/**
 * Generate WeChat HTML for 2026-05-15 (7-section layout)
 * Manual translation already applied to news JSON
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, 'data');
const newsFile = join(dataDir, 'news-2026-05-15.json');
const htmlFile = join(dataDir, 'wechat-html-2026-05-15.html');

const { news } = JSON.parse(readFileSync(newsFile, 'utf8'));
const date = '2026-05-15';

console.log('📄 Generating WeChat HTML (v5 compact style)...');

// Sort by score, take top 20 (we have exactly 20)
const sorted = news.sort((a, b) => (b.score || 0) - (a.score || 0));
const top = sorted.slice(0, 20);
const hl = top[0];

console.log(`📊 Total items: ${top.length}`);
console.log(`🏷️ Headline: ${hl.title_zh}`);

// Group by source (5 sections)
const sections = {
  '🔥 Hacker News': top.filter(n => n.source === 'HackerNews').slice(0, 5),
  '📰 TechCrunch': top.filter(n => n.source === 'TechCrunch').slice(0, 5),
  '🎙️ Latent Space': top.filter(n => n.source === 'LatentSpace').slice(0, 5),
  '💡 MIT Tech Review': top.filter(n => n.source === 'MITTechReview').slice(0, 5),
  '📡 The Decoder': top.filter(n => n.source === 'TheDecoder').slice(0, 5),
};

// Section colors (wechat-html-v5 inspired)
const colors = {
  '🔥 Hacker News': '#ff6b35',
  '📰 TechCrunch': '#1a73e8',
  '🎙️ Latent Space': '#9c27b0',
  '💡 MIT Tech Review': '#d32f2f',
  '📡 The Decoder': '#1976d2',
};

function smartTruncate(text, minLen, maxLen) {
  if (text.length <= maxLen) return text;
  const cut = text.substring(0, maxLen);
  const puncts = ['。', '？', '！', '；', '，', '.', '!', '?', ';'];
  let bestPos = -1;
  for (const p of puncts) {
    const pos = cut.lastIndexOf(p);
    if (pos > minLen && pos > bestPos) bestPos = pos;
  }
  if (bestPos !== -1) return text.substring(0, bestPos + 1);
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
    // Remove title prefix if present
    if (summary.startsWith(title)) {
      summary = summary.substring(title.length).trim();
    }
    // Clean up prefixes
    summary = summary.replace(/^[:：\s]+/, '').trim();

    // Target ~200 chars, truncate smartly
    if (summary.length > 200) {
      summary = smartTruncate(summary, 180, 200);
    } else if (summary.length < 150) {
      // Pad to reasonable minimum
      if (!summary.endsWith('。') && !summary.endsWith('.')) summary += '。';
    }
    summary = summary.trim();

    return `        <div style="padding:18px 0;border-bottom:1px solid #f0f0f0;line-height:1.55">
          <div style="font-size:16px;font-weight:700;margin-bottom:8px;color:#111">
            ${i + 1}. <a href="${n.url}" style="color:#1976d2;text-decoration:none">${title}</a>
          </div>
          <div style="font-size:14px;color:#555;line-height:1.6">${summary}</div>
        </div>`;
  }).join('');

  return `      <div style="margin:28px 0 0;">
        <h3 style="font-size:18px;font-weight:800;color:${color};margin:0 0 12px;padding-bottom:6px;border-bottom:2px solid ${color};display:flex;align-items:center;gap:8px">
          <span style="font-size:20px">${icon}</span> ${label}
        </h3>
        <div style="background:#fff;border:none;border-radius:0;padding:0;box-shadow:none">
${rows}
        </div>
      </div>`;
}

const body = Object.entries(sections).map(([name, items]) => sectionHTML(name, items)).filter(Boolean).join('\n');
const hlTitle = hl.title_zh || hl.title || 'AI News Daily';

const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>北美AI圈日报 ${date}</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;font-size:15px;line-height:1.6;color:#333;margin:0;padding:0;background:#fff;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased}
a{color:#1976d2;text-decoration:none;transition:color 0.2s}
a:hover{color:#0d47a1}
img{max-width:100%;border-radius:6px}
.header{text-align:center;padding:32px 20px 24px;background:linear-gradient(135deg,#f5f7fa 0%,#c3cfe2 100%);margin-bottom:8px}
.headline{font-size:26px;font-weight:800;color:#111;margin:10px 0 12px;line-height:1.35;letter-spacing:-0.3px}
.meta{font-size:13px;color:#666;margin-top:12px;letter-spacing:0.3px}
.section{margin:0 16px}
.footer{text-align:center;padding:28px 0 40px;color:#999;font-size:12px;border-top:1px solid #eee;margin-top:24px}
.footer p{margin:6px 0}
</style></head>
<body>
  <div class="header">
    <div class="headline">${hlTitle}</div>
    <div class="meta">${date} · 今日${top.length}条 · 来源：HackerNews TechCrunch LatentSpace MITTechReview</div>
  </div>

  <div class="section">
${body}
  </div>

  <div class="footer">
    <p>数据来源：Hacker News · TechCrunch · Latent Space · MIT Technology Review</p>
    <p style="margin-top:12px">由 AI News Publisher 自动生成 · Powered by OpenClaw</p>
  </div>
</body></html>`;

writeFileSync(htmlFile, html, 'utf8');
console.log(`✅ HTML generated: ${htmlFile}`);
console.log(`📊 Size: ${html.length} chars`);

// Verify section coverage
console.log('\n📋 Section coverage:');
Object.entries(sections).forEach(([name, items]) => {
  console.log(`   ${name.split(' ')[0]} ${name.split(' ').slice(1).join(' ')}: ${items.length} items`);
});

console.log(`\n📌 Headline: ${hlTitle}`);

export { generateHTML, selectImage };
