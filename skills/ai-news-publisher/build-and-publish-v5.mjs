#!/usr/bin/env node
/**
 * Generate WeChat HTML (v5.3 style) and publish
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, 'data');
const newsFile = join(dataDir, 'news-2026-05-12.json');
const htmlFile = join(dataDir, 'wechat-html-2026-05-12.html');

const { news } = JSON.parse(readFileSync(newsFile, 'utf8'));
const date = '2026-05-12';

console.log('📄 Generating WeChat HTML...');

// Sort by score, take top 15
const sorted = news.sort((a, b) => (b.score || 0) - (a.score || 0));
const top = sorted.slice(0, 15);
const hl = top[0];

// Sections (5 each)
const sections = {
  '🔥 Hacker News': top.filter(n => n.source === 'HackerNews').slice(0, 5),
  '📰 TechCrunch AI': top.filter(n => n.source === 'TechCrunch').slice(0, 5),
  '🎙️ Latent Space': top.filter(n => n.source === 'LatentSpace').slice(0, 5),
  '🤖 The Decoder': top.filter(n => n.source === 'TheDecoder').slice(0, 5),
  '💼 MIT Tech Review': top.filter(n => n.source === 'MITTechReview').slice(0, 5),
};

function sectionHTML(name, items) {
  if (!items.length) return '';
  const rows = items.map((n, i) => {
    const t = n.title_zh || n.title;
    const s = (n.summary_zh || '').substring(0, 140);
    return `      <div style="padding: 16px 0; border-bottom: 1px solid #f0f0f0;">
        <div style="font-size: 17px; font-weight: 700; color: #111; line-height: 1.5; margin-bottom: 8px;">
          <a href="${n.url}" style="text-decoration: none; color: #111;">${i + 1}. ${t}</a>
        </div>
        <div style="font-size: 14px; color: #555; line-height: 1.55; margin-top: 6px;">
          ${s}
        </div>
      </div>`;
  }).join('');
  return `    <div style="margin: 36px 0 0;">
      <h3 style="font-size: 20px; font-weight: 800; color: #e65100; margin: 0 0 16px; padding-bottom: 4px; border-bottom: 2px solid #e65100;">
        ${name}
      </h3>
      <div style="background: #fff; border: none; border-radius: 0; padding: 0 16px; box-shadow: none;">
${rows}
      </div>
    </div>`;
}

const body = Object.entries(sections).map(([n, i]) => sectionHTML(n, i)).filter(Boolean).join('\n');
const hlTitle = hl.title_zh || hl.title;

const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>北美AI圈日报 ${date}</title><style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;line-height:1.55;color:#333;margin:0;padding:0;background:#fff}.header{text-align:center;padding:30px 20px 20px;border-bottom:1px solid #e65100;margin-bottom:20px}.headline{font-size:26px;font-weight:800;color:#111;margin:10px 0 16px;line-height:1.4}.meta{font-size:13px;color:#888;margin-top:12px}.footer{text-align:center;padding:20px 0 40px;color:#aaa;font-size:12px;border-top:1px solid #eee;margin-top:30px}</style></head><body><div class="header"><div class="headline">${hlTitle}</div><div class="meta">${date} · 共${news.length}条 · HN/TC/LS/TD/MIT</div></div>
${body}<div class="footer"><p>数据来源：Hacker News · TechCrunch · Latent Space · The Decoder · MIT Technology Review</p><p style="margin-top:10px;">由 AI News Publisher 自动生成 · 每日07:00更新</p></div></body></html>`;

writeFileSync(htmlFile, html, 'utf8');
console.log(`✅ HTML generated: ${htmlFile}`);
console.log(`📊 Size: ${html.length} chars`);

// Verify headline
console.log(`\n📌 Headline: ${hlTitle}`);
console.log(`   Summary count: ${top.length}`);

// Publish
console.log('\n📤 Publishing to WeChat...');
try {
  const cmd = `WECHAT_APP_ID="wxa87b65ba78d3c822" WECHAT_APP_SECRET="ac6a029c2b4ef7c1b89fbaeeaace3931" node publish-article.mjs "${htmlFile}" "北美AI圈日报 ${date}" "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=640&h=400&fit=crop"`;
  const out = execSync(cmd, { cwd: __dirname, stdio: 'pipe', encoding: 'utf8', timeout: 30000 });
  console.log(out);
  const m = out.match(/Draft media_id[:：]\s*(\S+)/);
  if (m) {
    console.log(`\n🎉 SUCCESS! Draft created.`);
    console.log(`📎 Media ID: ${m[1]}`);
    console.log(`🔗 Manual publish required in WeChat backend`);
  }
} catch (e) {
  console.error('❌ Publish failed:', e.message);
}

console.log('\n✅ Done!');
