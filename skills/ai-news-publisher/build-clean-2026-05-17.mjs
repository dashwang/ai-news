#!/usr/bin/env node
/**
 * WeChat HTML generator — 纯中文排版，无英文原文链接
 * 2026-05-17
 */
import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, 'data');
const newsFile = join(dataDir, 'news-2026-05-17.json');
const htmlFile = join(dataDir, 'wechat-html-2026-05-17-cn.html');

const { news } = JSON.parse(readFileSync(newsFile, 'utf8'));
const date = '2026-05-17';
const HEADLINE = '离线语音转文字与 AI 键盘 · Today in AI';

console.log('📄 生成纯中文版 HTML…');

const sorted = news.sort((a, b) => (b.score || 0) - (a.score || 0));
const top = sorted.slice(0, 15);
const hlTitle = top[0].title_zh || top[0].title;

// Section config: 中文名 · 条数 · 颜色
const sectionCfg = [
  { name: 'TechCrunch AI',      color: '#1a73e8', items: top.filter(n => n.source === 'TechCrunch') },
  { name: 'Hacker News',        color: '#ff6b35', items: top.filter(n => n.source === 'HackerNews') },
  { name: 'Substack',           color: '#9c27b8', items: top.filter(n => n.source === 'LatentSpace' || n.source === 'TheDecoder' || n.source === 'MITTechReview') },
];

function sectionHTML({ name, color, items }) {
  if (!items.length) return '';
  const rows = items.map((n, i) => {
    const t = n.title_zh || n.title;
    const s = (n.summary_zh || '').replace(/\s+/g, ' ').trim();
    // 纯文字标题，不设链接
    const topTag = n.source === 'HackerNews' && n.score > 1
      ? `<span style="display:inline-block;background:#ff6b35;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;margin-left:8px;font-weight:400">🔥 ${n.score > 2 ? '热门' : '热议'}</span>`
      : '';
    return `      <div style="padding: 18px 0 ${items.length - 1 === i ? '0' : '10px'}; border-bottom: 1px solid #f5f5f5;">
        <div style="font-size: 16px; font-weight: 700; color: #111; line-height: 1.55; margin-bottom: 8px;">
          ${i + 1}. ${t}${topTag}
        </div>
        <div style="font-size: 14px; color: #666; line-height: 1.7; margin-top: 4px;">
          ${s}
        </div>
      </div>`;
  }).join('\n');
  return `    <div style="margin: 32px 0 0;">
      <h3 style="font-size: 19px; font-weight: 800; color: ${color}; margin: 0 0 14px; padding-bottom: 6px; border-bottom: 2px solid ${color};">
        ${name}
      </h3>
      <div style="padding: 0 2px;">
${rows}
      </div>
    </div>`;
}

const sectionsHTML = sectionCfg
  .map(cfg => sectionHTML(cfg))
  .filter(Boolean)
  .join('\n');

const total = sectionCfg.reduce((sum, c) => sum + c.items.length, 0);

const html = `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AI 日报 · ${date}</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
     line-height:1.6;color:#333;margin:0;padding:0;background:#fff}
img{max-width:100%;border-radius:8px}
</style>
</head>
<body>

<!-- ═══ 顶部头条 ═══ -->
<div style="text-align:center;padding:30px 16px 24px;
     border-bottom:3px solid #e65100;margin-bottom:0">
  <div style="font-size:22px;font-weight:800;color:#111;
       line-height:1.4;margin-bottom:12px">${hlTitle}</div>
  <div style="font-size:13px;color:#888">${date} · 今日 ${total} 条精选</div>
</div>

${sectionsHTML}

<!-- ═══ 底部 ═══ -->
<div style="text-align:center;padding:32px 0 48px;
     color:#aaa;font-size:12px;border-top:1px solid #eee;margin-top:36px">
  <p style="margin:0 0 6px;letter-spacing:0.5px">
    数据来源：Hacker News · TechCrunch · Latent Space · The Decoder · MIT Tech Review
  </p>
  <p style="margin:0">由 AI News Publisher · 每日自动生成</p>
</div>

</body></html>`;

writeFileSync(htmlFile, html, 'utf8');
console.log(`✅ HTML 已生成：${htmlFile}`);
console.log(`📊 大小：${html.length} 字符，${top.length} 条精选`);
console.log(`📌 头条：${hlTitle}`);
