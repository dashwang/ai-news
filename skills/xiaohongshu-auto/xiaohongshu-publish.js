/**
 * 小红书自动化发布脚本
 * 使用 Playwright
 * 
 * 需要先安装: npm install playwright
 * 
 * 使用方法:
 *   node xiaohongshu-publish.js --content "你的内容" --image "图片路径"
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  // 小红书创作者中心
  creatorUrl: 'https://creator.xiaohongshu.com/publish/publisharticle',
  // 登录页
  loginUrl: 'https://www.xiaohongshu.com/explore',
  // Cookie 存储文件
  cookieFile: './xiaohongshu_cookies.json',
};

async function loginAndGetCookies() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  console.log('📱 请扫码登录小红书...');
  
  await page.goto(CONFIG.loginUrl);
  
  // 等待用户扫码登录
  await page.waitForURL('**/creator.xiaohongshu.com/**', { timeout: 120000 });
  
  console.log('✅ 登录成功！');
  
  // 保存 cookies
  const cookies = await context.cookies();
  fs.writeFileSync(CONFIG.cookieFile, JSON.stringify(cookies, null, 2));
  console.log('💾 Cookies 已保存');
  
  return { browser, context, page };
}

async function loadCookies() {
  if (!fs.existsSync(CONFIG.cookieFile)) {
    return null;
  }
  const cookies = JSON.parse(fs.readFileSync(CONFIG.cookieFile, 'utf-8'));
  return cookies;
}

async function publishArticle(title, content, imagePath = null) {
  console.log('🚀 开始发布...');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  
  // 尝试加载 cookies
  const savedCookies = await loadCookies();
  if (savedCookies) {
    await context.addCookies(savedCookies);
    console.log('📂 已加载保存的 Cookies');
  }
  
  const page = await context.newPage();
  
  // 如果没有 cookies，需要扫码登录
  if (!savedCookies) {
    console.log('📱 请扫码登录...');
    await page.goto(CONFIG.loginUrl);
    await page.waitForURL('**/creator.xiaohongshu.com/**', { timeout: 120000 });
    const cookies = await context.cookies();
    fs.writeFileSync(CONFIG.cookieFile, JSON.stringify(cookies, null, 2));
  }
  
  // 跳转到发布页
  await page.goto(CONFIG.creatorUrl);
  await page.waitForLoadState('networkidle');
  
  // 输入标题
  console.log('✍️ 输入标题...');
  await page.fill('input[placeholder*="标题"]', title);
  
  // 输入正文
  console.log('✍️ 输入正文...');
  await page.fill('.note-textarea', content);
  
  // 如果有图片，尝试上传
  if (imagePath && fs.existsSync(imagePath)) {
    console.log('📷 上传图片...');
    const fileInput = await page.$('input[type="file"]');
    if (fileInput) {
      await fileInput.setInputFiles(imagePath);
    }
  }
  
  // 等待一下让内容加载
  await page.waitForTimeout(2000);
  
  console.log('✅ 内容已填入，请在浏览器中确认并点击发布');
  console.log('⏰ 等待 30 秒让你确认...');
  
  await page.waitForTimeout(30000);
  
  // 可以选择自动点击发布按钮（谨慎使用）
  // await page.click('button:has-text("发布")');
  
  await browser.close();
  console.log('🏁 完成！');
}

// CLI 参数解析
const args = process.argv.slice(2);
let title = 'AI 时代：两天做出产品，用户破千！';
let content = '';
let image = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--content' && args[i + 1]) {
    content = args[i + 1];
  }
  if (args[i] === '--title' && args[i + 1]) {
    title = args[i + 1];
  }
  if (args[i] === '--image' && args[i + 1]) {
    image = args[i + 1];
  }
}

// 如果没有提供内容，使用默认
if (!content) {
  content = `用AI做产品太香了！🤩

两天搞定😱用户破千！

姐妹们！今天必须分享这个！

一个前字节的工程师
以前从没写过客户端代码🙈

用AI两天做出了一个产品👇

就是它👉 OneClaw

现在几千用户在用🤯

关键是！！！

💡 AI不只是一个聊天工具
它更像一个数字员工！

现在就开始学起来！🦞

#AI #副业 #创业`;
}

// 执行
publishArticle(title, content, image).catch(console.error);
