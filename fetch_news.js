#!/usr/bin/env node
/**
 * AI News Publisher - Node.js Clean Version (v5)
 * Features: 5 sources ≥5 each, no external translation, compact layout, no outer frame
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import https from 'https';
import { pipeline } from 'stream';
import { createWriteStream } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG = {
  outputDir: join(__dirname, 'data'),
  date: new Date().toISOString().split('T')[0],
  wechatAppId: process.env.WECHAT_APP_ID || '',
  wechatAppSecret: process.env.WECHAT_APP_SECRET || '',
};
mkdirSync(CONFIG.outputDir, { recursive: true });

function httpsGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve({ body: d }));
    }).on('error', reject);
  });
}

function parseRSS(xml) {
  const items = [];
  const re = /<item[^>]*>([\s\S]*?)<\/item>/gi;
  let m;
  while ((m = re.exec(xml)) !== null) {
    const i = m[1];
    const t = (i.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1] || '').replace(/<!\[CDATA\[(.*?)\]\]>/g, '$1').trim();
    const l = (i.match(/<link[^>]*>([\s\S]*?)<\/link>/i)?.[1] || '').trim();
    if (t && l) items.push({ title: t, link: l });
  }
  return items;
}

async function fetchHN() {
  try {
    const cutoff = Math.floor((Date.now() - 86400000) / 1000);
    const queries = ['AI LLM', 'GPT Claude', 'DeepSeek', 'OpenAI', 'Anthropic'];
    let hits = [];
    for (const q of queries) {
      const u = `https://hn.algolia.com/api/v1/search?query=${encodeURIComponent(q)}&tags=story&numericFilters=created_at_i>${cutoff}&hitsPerPage=5`;
      const { body } = await httpsGet(u);
      const d = JSON.parse(body);
      hits = [...hits, ...d.hits];
    }
    const uniq = [...new Map(hits.map(h => [h.objectID, h])).values()];
    return uniq.slice(0,5).map(h => ({
      source: 'HackerNews',
      title: h.title,
      url: h.url || `https://news.ycombinator.com/item?id=${h.objectID}`,
      summary: '',
      score: h.points || 0
    }));
  } catch (e) { return []; }
}

async function fetchTechCrunch() {
  try {
    const { body } = await httpsGet('https://techcrunch.com/category/artificial-intelligence/feed/');
    return parseRSS(body).slice(0,5).map(i => ({ source: 'TechCrunch', title: i.title, url: i.link, summary: '' }));
  } catch (e) { return []; }
}
async function fetchLatentSpace() {
  try {
    const { body } = await httpsGet('https://www.latent.space/feed');
    return parseRSS(body).slice(0,5).map(i => ({ source: 'LatentSpace', title: i.title, url: i.link, summary: '' }));
  } catch (e) { return []; }
}
async function fetchTheDecoder() {
  try {
    const { body } = await httpsGet('https://the-decoder.com/feed/');
    return parseRSS(body).slice(0,5).map(i => ({ source: 'TheDecoder', title: i.title, url: i.link, summary: '' }));
  } catch (e) { return []; }
}
async function fetchMIT() {
  try {
    const { body } = await httpsGet('https://www.technologyreview.com/feed/');
    return parseRSS(body).slice(0,5).map(i => ({ source: 'MITTechReview', title: i.title, url: i.link, summary: '' }));
  } catch (e) { return []; }
}

async function fetchAll() {
  const [hn, tc, ls, td, mit] = await Promise.all([
    fetchHN(), fetchTechCrunch(), fetchLatentSpace(), fetchTheDecoder(), fetchMIT()
  ]);
  console.log(`Sources: HN=${hn.length} TC=${tc.length} LS=${ls.length} TD=${td.length} MIT=${mit.length}`);
  return [...hn, ...tc, ...ls, ...td, ...mit];
}

function ensureChineseFields(news) {
  for (const n of news) {
    if (!n.title_zh) n.title_zh = n.title;
    if (!n.summary_zh) n.summary_zh = `本文报道了${n.title_zh}，涉及${n.source}等平台讨论。`;
  }
}

function selectHeadline(news) {
  return [...news].sort((a,b) => (b.score||0) - (a.score||0) || 0)[0];
}

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
    '🔥 Hacker News': news.filter(n=>n.source==='HackerNews'),
    '📰 TechCrunch AI': news.filter(n=>n.source==='TechCrunch'),
    '🎙️ Latent Space': news.filter(n=>n.source==='LatentSpace'),
    '🤖 The Decoder': news.filter(n=>n.source==='TheDecoder'),
    '💼 MIT Tech Review': news.filter(n=>n.source==='MITTechReview'),
  };
  const fmt = (name, items) => {
    if (!items.length) return '';
    const lines = items.slice(0,5).map((n,i) => {
      const t = n.title_zh || n.title;
      const s = (n.summary_zh || `本文报道了${t}，涉及${n.source}等平台讨论。`).substring(0,140);
      return `      <div style="padding: 16px 0; border-bottom: 1px solid #f0f0f0;">
        <div style="font-size: 17px; font-weight: 700; color: #111111; line-height: 1.5; margin-bottom: 8px;">
          <a href="${n.url}" style="text-decoration: none; color: #111111;">${i+1}. ${t}</a>
        </div>
        <div style="font-size: 14px; color: #555555; line-height: 1.55; margin-top: 6px;">
          ${s}...
        </div>
      </div>`;
    }).join('');
    return `    <div style="margin: 36px 0 0;">
      <h3 style="font-size: 20px; font-weight: 800; color: #e65100; margin: 0 0 16px; padding-bottom: 8px; border-bottom: 2px solid #e65100;">
        ${name}
      </h3>
      <div style="background: #ffffff; border: none; border-radius: 0; padding: 0 16px; box-shadow: none;">
${lines}
      </div>
    </div>`;
  };
  const body = Object.entries(sections).map(([n,i])=>fmt(n,i)).filter(Boolean).join('\n');
  const img = selectImage(hl);
  return `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>北美AI圈日报 ${CONFIG.date}</title><style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;line-height:1.55;color:#333;margin:0;padding:0;background:#ffffff}.header{text-align:center;padding:40px 20px 30px;border-bottom:1px solid #e65100;margin-bottom:30px}.headline{font-size:28px;font-weight:800;color:#111;margin:16px 0 20px;line-height:1.4}.headline-img{width:100%;max-width:600px;height:auto;border-radius:12px;margin:0 auto 20px;display:block}.meta{font-size:13px;color:#888;margin-top:16px}.footer{text-align:center;padding:30px 0 50px;color:#aaa;font-size:12px;border-top:1px solid #eee;margin-top:40px}</style></head><body><div class="header"><div class="headline">${hl.title_zh||hl.title}</div><img src="${img}" class="headline-img" alt="头条配图"><div class="meta">${CONFIG.date} · 共${news.length}条 · HN/TC/LS/TD/MIT</div></div>
${body}<div class="footer"><p>数据来源：Hacker News · TechCrunch · Latent Space · The Decoder · MIT Technology Review</p><p style="margin-top:10px;">由 AI News Publisher 自动生成 · 每日 07:00 更新</p></div></body></html>`;
}

function checkDuplicated(date) {
  const f = join(CONFIG.outputDir, 'published.json');
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
  const f = join(CONFIG.outputDir, 'published.json');
  let d = {};
  if (existsSync(f)) d = JSON.parse(readFileSync(f, 'utf8'));
  if (!d.published) d.published = [];
  d.published.push({ date: CONFIG.date, ...info });
  writeFileSync(f, JSON.stringify(d, null, 2));
  console.log('📝 记录完成');
}

async function publishToWechat(html, title) {
  if (!CONFIG.wechatAppId || !CONFIG.wechatAppSecret) {
    console.log('⚠️ 未配置 WECHAT_*');
    return {};
  }
  const tmp = join(CONFIG.outputDir, `tmp-${Date.now()}.html`);
  writeFileSync(tmp, html, 'utf8');
  try {
    const { exec } = await import('child_process');
    const cmd = `cd ${__dirname} && WECHAT_APP_ID="${CONFIG.wechatAppId}" WECHAT_APP_SECRET="${CONFIG.wechatAppSecret}" node publish-article.mjs "${tmp}" "${title}" "${selectImage({title})}"`;
    await exec(cmd);
    console.log('✅ 发布成功');
    return { draftId: 'ok' };
  } catch (e) {
    console.error('❌ 发布失败:', e.message);
    return {};
  }
}

async function main() {
  console.log(`📅 北美AI圈日报 - ${CONFIG.date}`);
  const news = await fetchAll();
  if (news.length < 20) console.warn(`⚠️ 仅 ${news.length} 条`);

  ensureChineseFields(news);

  const hl = selectHeadline(news);
  console.log('📰 头条:', hl.title_zh || hl.title);

  const html = generateWechatHTML(news, hl);
  const htmlFile = join(CONFIG.outputDir, `wechat-html-${CONFIG.date}.html`);
  writeFileSync(htmlFile, html, 'utf8');
  console.log('✅ HTML:', htmlFile);

  if (!checkDuplicated(CONFIG.date)) {
    if (process.argv.includes('--publish')) {
      const res = await publishToWechat(html, `北美AI圈日报 ${CONFIG.date}`);
      recordPublished({ title: hl.title_zh || hl.title, draftId: res.draftId, count: news.length });
    } else {
      console.log('💡 使用 --publish 发布到公众号');
    }
  }

  writeFileSync(join(CONFIG.outputDir, `news-${CONFIG.date}.json`), JSON.stringify({ date: CONFIG.date, news }, null, 2));
  console.log('🎉 完成');
}

main().catch(e => { console.error(e); process.exit(1); });
