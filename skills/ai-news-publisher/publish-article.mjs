#!/usr/bin/env node
import { readFileSync, createWriteStream, unlinkSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import https from 'https';
import FormData from 'form-data';

const __dirname = dirname(fileURLToPath(import.meta.url));

let WECHAT_APP_ID = process.env.WECHAT_APP_ID;
let WECHAT_APP_SECRET = process.env.WECHAT_APP_SECRET;

if (!WECHAT_APP_ID || !WECHAT_APP_SECRET) {
  try {
    const dotenv = readFileSync(join(__dirname, '.env'), 'utf8');
    for (const line of dotenv.split('\n')) {
      if (line.startsWith('WECHAT_APP_ID=')) WECHAT_APP_ID = line.split('=',2)[1].trim();
      if (line.startsWith('WECHAT_APP_SECRET=')) WECHAT_APP_SECRET = line.split('=',2)[1].trim();
    }
  } catch(e) {}
}

if (!WECHAT_APP_ID || !WECHAT_APP_SECRET) {
  console.log('❌ Missing WECHAT_APP_ID/SECRET');
  process.exit(1);
}

const [htmlFile, title, coverUrl] = process.argv.slice(2);
if (!htmlFile || !title) {
  console.log('Usage: node publish-article.mjs <html_file> <title> [cover_image_url]');
  process.exit(1);
}

function httpsGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve({ body: d, statusCode: res.statusCode }));
    }).on('error', reject);
  });
}

async function getToken() {
  const { body } = await httpsGet(`https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${WECHAT_APP_ID}&secret=${WECHAT_APP_SECRET}`);
  const d = JSON.parse(body);
  if (d.access_token) return d.access_token;
  throw new Error(`Token error: ${body}`);
}

/**
 * 上传封面图，返回 { media_id, url }
 */
async function uploadImage(token, imageUrl) {
  const imgPath = join(__dirname, 'data', `cover-${Date.now()}.jpg`);
  const file = createWriteStream(imgPath);
  const resp = await new Promise((resolve, reject) => {
    https.get(imageUrl, res => {
      if (res.statusCode !== 200) reject(new Error(`HTTP ${res.statusCode}`));
      else resolve(res);
    }).on('error', reject);
  });
  await new Promise((resolve, reject) => {
    resp.pipe(file);
    file.on('finish', resolve);
    file.on('error', reject);
  });

  const form = new FormData();
  form.append('media', readFileSync(imgPath), { filename: 'cover.jpg', contentType: 'image/jpeg' });
  const length = await new Promise((resolve, reject) => {
    form.getLength((err, len) => err ? reject(err) : resolve(len));
  });

  const uploadUrl = `https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${token}&type=image`;
  const { body: respBody } = await new Promise((resolve, reject) => {
    const req = https.request(uploadUrl, {
      method: 'POST',
      headers: Object.assign({}, form.getHeaders(), { 'Content-Length': length })
    }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve({ body: d }));
    });
    req.on('error', reject);
    form.pipe(req);
  });
  unlinkSync(imgPath);
  const d = JSON.parse(respBody);
  if (d.media_id) return { media_id: d.media_id, url: d.url || '' };
  throw new Error(`Upload failed: ${d.errmsg}`);
}

/**
 * 上传正文插图，返回微信 CDN URL
 */
async function uploadBodyImage(token, remoteUrl) {
  const imgPath = join(__dirname, 'data', `body-${Date.now()}.jpg`);
  const file = createWriteStream(imgPath);
  const resp = await new Promise((resolve, reject) => {
    https.get(remoteUrl, res => {
      if (res.statusCode !== 200) throw new Error(`IMG HTTP ${res.statusCode}: ${remoteUrl}`);
      else resolve(res);
    }).on('error', reject);
  });
  await new Promise((resolve, reject) => {
    resp.pipe(file);
    file.on('finish', resolve);
    file.on('error', reject);
  });

  const form = new FormData();
  form.append('media', readFileSync(imgPath), {
    filename: 'article-img-' + Date.now() + '.jpg',
    contentType: 'image/jpeg'
  });
  const length = await new Promise((resolve, reject) => {
    form.getLength((err, len) => err ? reject(err) : resolve(len));
  });

  const uploadUrl = `https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${token}&type=image`;
  const { body: respBody } = await new Promise((resolve, reject) => {
    const req = https.request(uploadUrl, {
      method: 'POST',
      headers: Object.assign({}, form.getHeaders(), { 'Content-Length': length })
    }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve({ body: d }));
    });
    req.on('error', reject);
    form.pipe(req);
  });
  unlinkSync(imgPath);
  const d = JSON.parse(respBody);
  if (d.url) return d.url;
  throw new Error(`Body upload failed: ${d.errmsg}`);
}

/**
 * 提取 HTML 中所有 <img src="..."> 的唯一远程 URL
 */
function extractImageUrls(html) {
  const seen = {};
  const out = [];
  const re = /<img\s+src="(https?:\/\/[^"]+)"/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    const url = m[1];
    if (!seen[url]) {
      seen[url] = true;
      out.push(url);
    }
  }
  return out;
}

/**
 * 将所有远程 img src 替换为微信 CDN 地址
 */
async function resolveBodyImages(token, html) {
  const urls = extractImageUrls(html);
  if (urls.length === 0) return html;
  console.log(`📸 ${urls.length} body images → uploading to WeChat CDN…`);
  const map = {};
  for (const url of urls) {
    try {
      const wxUrl = await uploadBodyImage(token, url);
      map[url] = wxUrl;
      console.log(`  ✓ ${url.split('/').pop()} → ${wxUrl.substring(0, 55)}…`);
    } catch(e) {
      console.log(`  ⚠️ skip ${url.split('/').pop()}: ${e.message}`);
    }
  }
  let result = html;
  for (const [remote, wx] of Object.entries(map)) {
    result = result.split(remote).join(wx);
  }
  return result;
}

function extractFirstLink(html) {
  const match = html.match(/href="([^"]+?)"/i);
  return match ? match[1] : 'https://news.ycombinator.com';
}

async function createDraft(token, html, title, mediaId) {
  const sourceUrl = extractFirstLink(html);
  const article = {
    title: title.substring(0, 30),
    author: 'AI News',
    content: html,
    digest: '深度学习社区精选',
    thumb_media_id: mediaId,
    show_cover_pic: 1,
    content_source_url: sourceUrl
  };
  const payload = { articles: [article] };
  const data = JSON.stringify(payload);
  console.log(`Draft: titleLen=${article.title.length}, contentLen=${article.content.length}`);

  const { body: respBody, statusCode } = await new Promise((resolve, reject) => {
    const req = https.request(
      `https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${token}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(data) }
      },
      res => {
        let d = '';
        res.on('data', c => d += c);
        res.on('end', () => resolve({ body: d, statusCode: res.statusCode }));
      }
    );
    req.on('error', reject);
    req.write(data);
    req.end();
  });
  console.log(`HTTP ${statusCode}: ${respBody.substring(0, 150)}`);
  const d = JSON.parse(respBody);
  if (d.media_id) return d.media_id;
  if (d.errcode === 0) return d.media_id;
  throw new Error(`Draft error ${d.errcode || 'unknown'}: ${d.errmsg || 'no media_id'}`);
}

async function main() {
  console.log('== WeChat Publisher v2 (body image → CDN) ==');
  const html = readFileSync(htmlFile, 'utf8');
  console.log(`HTML: ${htmlFile}, size: ${html.length}`);
  console.log(`Title: ${title}`);

  const token = await getToken();
  console.log(`Token OK`);

  // Step 1: upload cover
  const cover = coverUrl || 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80';
  const { media_id: coverMediaId, url: coverThumb } = await uploadImage(token, cover);
  console.log(`Cover media_id: ${coverMediaId}${coverThumb ? ' · url=' + coverThumb.substring(0,60) : ''}`);

  // Step 2: replace body images
  const htmlWithWxImages = await resolveBodyImages(token, html);

  // Step 3: create draft
  const draftId = await createDraft(token, htmlWithWxImages, title, coverMediaId);
  console.log(`Draft media_id: ${draftId}`);

  // Step 4: auto-publish (best-effort)
  try {
    const pubUrl = `https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=${token}`;
    const { body: pubBody } = await new Promise((resolve, reject) => {
      const data = JSON.stringify({ media_id: draftId });
      const req = https.request(pubUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
      }, res => {
        let d = '';
        res.on('data', c => d += c);
        res.on('end', () => resolve({ body: d }));
      });
      req.on('error', reject);
      req.write(data);
      req.end();
    });
    const pub = JSON.parse(pubBody);
    if (pub.errcode === 0) console.log('✅ Auto-published');
    else console.log(`⚠️ Draft ready, auto-publish ${pub.errcode}: ${pub.errmsg}`);
  } catch(e) {
    console.log('⚠️ Auto-publish skipped');
  }
  console.log('Done');
}

main().catch(e => {
  console.error('❌', e.message);
  process.exit(1);
});
