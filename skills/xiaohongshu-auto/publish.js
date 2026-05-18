/**
 * 小红书自动化发布脚本 (服务器版)
 * 使用 Playwright (headless)
 */

const { chromium } = require('playwright');
const fs = require('fs');

const CONFIG = {
  creatorUrl: 'https://creator.xiaohongshu.com/publish/publisharticle',
  loginUrl: 'https://www.xiaohongshu.com/explore',
  cookieFile: './xiaohongshu_cookies.json',
};

async function loadCookies() {
  if (!fs.existsSync(CONFIG.cookieFile)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(CONFIG.cookieFile, 'utf-8'));
}

async function publishArticle(title, content) {
  console.log('🚀 开始发布...');
  
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/chromium',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext();
  const savedCookies = await loadCookies();
  
  if (savedCookies.length > 0) {
    await context.addCookies(savedCookies);
    console.log('📂 已加载 Cookies');
  }
  
  const page = await context.newPage();
  
  if (savedCookies.length === 0) {
    console.log('📱 首次运行：请扫码登录...');
    await page.goto(CONFIG.loginUrl);
    console.log('⏳ 等待登录...（请扫码，5分钟超时）');
    try {
      await page.waitForURL('**/creator.xiaohongshu.com/**', { timeout: 300000 });
      console.log('✅ 登录成功！');
    } catch (e) {
      await page.screenshot({ path: 'login_timeout.png' });
      await browser.close();
      return { success: false, message: '登录超时' };
    }
    const cookies = await context.cookies();
    fs.writeFileSync(CONFIG.cookieFile, JSON.stringify(cookies, null, 2));
    console.log('💾 Cookies 已保存');
  }
  
  console.log('📝 跳转发布页...');
  await page.goto(CONFIG.creatorUrl);
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'publish_page.png' });
  console.log('📸 截图: publish_page.png');
  
  await page.waitForTimeout(3000);
  
  // 尝试输入内容
  const selectors = ['.note-textarea', 'textarea[placeholder*="正文"]', 'div[contenteditable="true"]'];
  for (const sel of selectors) {
    try {
      const el = await page.$(sel);
      if (el) {
        await el.fill(content);
        console.log('✅ 内容已填入');
        break;
      }
    } catch (e) {}
  }
  
  await page.screenshot({ path: 'content_filled.png' });
  console.log('📸 内容截图: content_filled.png');
  
  await browser.close();
  console.log('🏁 完成！请检查截图并在浏览器中确认发布');
  return { success: true };
}

const content = `用AI做产品太香了！🤩

两天搞定😱用户破千！

一个前字节的工程师
以前从没写过客户端代码

用AI两天做出了一个产品👇

就是它👉 OneClaw

现在几千用户在用🤯

关键是！！！

💡 AI不只是一个聊天工具
它更像一个数字员工！

现在就开始学起来！🦞

#AI #副业 #创业`;

const title = '用AI做产品太香了！两天搞定，用户破千！';

publishArticle(title, content).then(r => {
  console.log('结果:', r);
  process.exit(0);
}).catch(e => {
  console.error('错误:', e);
  process.exit(1);
});
