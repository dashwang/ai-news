/**
 * 小红书登录脚本
 * 只需运行一次，保存登录态
 */

const { chromium } = require('playwright');
const fs = require('fs');

async function main() {
  console.log('🚀 启动浏览器...');
  
  // 打开浏览器（会弹出窗口）
  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 100
  });
  
  const context = await browser.newContext();
  const page = await context.newPage();
  
  console.log('📱 请扫码登录小红书...');
  
  // 打开小红书
  await page.goto('https://www.xiaohongshu.com/explore');
  
  // 等待扫码登录成功（检测到进入创作者中心）
  try {
    await page.waitForURL('**/creator.xiaohongshu.com/**', { timeout: 300000 });
    console.log('✅ 登录成功！');
  } catch (e) {
    console.log('❌ 登录超时，请重试');
    await browser.close();
    process.exit(1);
  }
  
  // 保存 cookies
  const cookies = await context.cookies();
  fs.writeFileSync('xiaohongshu_cookies.json', JSON.stringify(cookies, null, 2));
  
  console.log('✅ Cookies 已保存到: xiaohongshu_cookies.json');
  console.log('📧 请把这个文件发给小龙虾 🦞');
  
  // 等待一下让用户看到消息
  await page.waitForTimeout(2000);
  
  await browser.close();
}

main();
