const { chromium } = require('playwright');

(async () => {
  console.log('启动浏览器...');
  try {
    const browser = await chromium.launch({
      headless: true,
      executablePath: '/usr/bin/chromium',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    console.log('✅ 浏览器启动成功');
    
    const page = await browser.newPage();
    console.log('✅ 页面创建成功');
    
    await page.goto('https://www.xiaohongshu.com');
    console.log('✅ 页面加载成功');
    console.log('标题:', await page.title());
    
    await browser.close();
    console.log('✅ 完成');
  } catch (e) {
    console.error('❌ 错误:', e.message);
  }
})();
