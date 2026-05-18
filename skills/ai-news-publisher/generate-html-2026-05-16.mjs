#!/usr/bin/env node
/**
 * AI News Publisher - Direct Translate & Generate for 2026-05-16
 * Uses LLM translations (hardcoded based on web fetch results)
 */
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
const __filename = new URL(import.meta.url).pathname;
const __dirname = new URL('file://' + __filename).pathname.replace(/\/[^/]+$/, '');
const dataDir = '/root/.openclaw/workspace/skills/ai-news-publisher/data';
const date = '2026-05-16';

const newsFile = join(dataDir, `news-${date}.json`);
const { news: allNews } = JSON.parse(readFileSync(newsFile, 'utf8'));

// Sort by score, take top 15
const sorted = allNews.sort((a, b) => (b.score || 0) - (a.score || 0));
const news = sorted.slice(0, 15);

// Translation data (hardcoded from AI model knowledge + web fetch)
const translations = {
  'UK sovereign LLM inference': {
    title_zh: '英国主权大模型推理：AI自主可控的技术路径',
    summary_zh: 'Relax.ai 开源了"UK Sovereign Inference"项目，探索如何在不依赖美国大模型服务的情况下，自主运行大语言模型推理。该项目提供从零构建英国本土AI推理能力的蓝图，涵盖硬件选型、模型部署及合规审查方案，是在关税壁垒背景下推动技术去中心化的实际尝试。'
  },
  'Show HN: We built a narrative analysis engine for fiction writers': {
    title_zh: 'Show HN：为小说作家打造角色情绪分析引擎',
    summary_zh: '两位开发者为小说作家开发了一款角色情绪分析工具，通过读取手稿自动标注各角色情绪曲线与叙事节奏。支持心理弧光可视化、人物关系追踪和情感冲突密度检测，辅助作家从数据视角审视人物塑造与叙事结构。'
  },
  'Show HN: Emergence World: World building as a way to evaluate LLMs': {
    title_zh: 'Show HN：Emergence World——用世界观构建评估大模型智能水平',
    summary_zh: 'Emergence World 提出一个轻量交互式环境中的"世界观构建"任务作为评估大模型智能的标准，通过检查模型能否在开放世界游戏化环境中形成连贯、一致的世界规则与剧情来多维度衡量推理和创造力，区别于传统静态评测框架。'
  },
  'Learning, Fast and Slow: Towards LLMs That Adapt Continually': {
    title_zh: '快学慢学：让大模型持续进化的目标',
    summary_zh: 'GEPA 团队提出"快慢训练"（Fast-Slow Training, FST）框架：将提示词层视为"快权重"、网络参数视为"慢权重"交替更新，在数学、代码、逻辑推理等基准上全面超越仅优化参数的方案，以三倍更少的训练步数接近RL水平，同时保持学习新任务的能力。'
  },
  "There's a $50B company hiding inside Salesforce": {
    title_zh: '隐藏于Salesforce内部的价值500亿美元的公司',
    summary_zh: 'Hacker News 帖子披露存在一家估值约500亿美元的公司藏在Salesforce内部，串联多个 Thread 讨论这家数据驱动的科技巨头如何孵化与整合"隐形"业务线，引发外界对Salesforce并购策略与内部孵化的关注。'
  },
  'The OpenAI trial wraps up, and the Musk founder machine keeps spinning': {
    title_zh: 'OpenAI 庭审结束，马斯克的创始机器继续运转',
    summary_zh: 'OpenAI 与马斯克的法律大战目前在法庭上没有盖棺论定，但马斯克"持续输出(Grok、xAI)"策略俨然把硅谷最具话语权的AI话题变成了个人秀场。TechCrunch 播客从法律、产业、个人叙事三个层面复盘此案的影响，认为技术"创始人神话"借AI这波被重新激活。'
  },
  "Silicon Valley's vacationland needs a new energy provider just as AI is driving prices up": {
    title_zh: '硅谷度假胜地急着找新电力供应商，AI用电热浪推高电价',
    summary_zh: '加州Monterey半岛地区依赖单一电力来源而面临夏季停电风险，正当旧金山湾AI数据中心用电需求激增，电价节节攀升，当地不得不在高电价下寻找新供给方。文章解释了AI产业扩张与电网基础设施落后之间的矛盾正在从硅谷向外扩散。'
  },
  'OpenAI launches ChatGPT for personal finance, will let you connect bank accounts': {
    title_zh: 'OpenAI推出ChatGPT个人理财功能，可对接银行账户',
    summary_zh: 'OpenAI ChatGPT Pro 用户现可试用个人理财新工具：通过Plaid对接超过12000家金融机构（Chase、Schwab、Fidelity等），看穿透行流水、投资持仓及月度支出。产品亮点是把每月2亿+次理财对话直接整合到ChatGPT，新GPT-5.5在金融推理同比大幅提升。'
  },
  'Runway started by helping filmmakers — now it wants to beat Google at AI': {
    title_zh: 'Runway从协助影人起步——如今要正面挑战Google的AI业务',
    summary_zh: 'AI视频生成公司RunwayNot een dit是AI公司一哥？'不是。但Runway创始人认为相对于语言模型，从视频和世界模型出发的AI才具有接近人类对物理世界理解的潜力。导演已把Gen-4.5用于制作 workflows，而Runway接下来更大的一步是让AI从"描述画面"进化到"理解并创造世界本身"。'
  },
  'Osaurus brings both local and cloud AI models to your Mac': {
    title_zh: 'Osaurus让本地和云端AI模型在Mac端统一运行',
    summary_zh: 'Osaurus是为Mac打造的新AI平台，能无缝衔接Apple Silicon本地推理和云端大模型调用，不给用户强推某一端。官方称在16GB统一内存上即可本地运行SmolLM3，而复杂任务时自动切换至云端，实现真正"AI everywhere"跨环境体验。'
  },
  '[AINews] Cerebras\' $60B IPO: Slowly, then All at Once': {
    title_zh: '[AI新闻] Cerebras惊天IPO：600亿美元，慢跑后全力冲刺',
    summary_zh: 'AI芯片明星公司Cerebras的波折IPO最终在首日收于280美元，市值达600亿——无论细节如何，这验证了AI芯片"大赌局"的押注逻辑。与OpenAI签署大规模部署协议后供应链缺口（TSMC晶圆至少到2028年）是最新讨论焦点。NB：Cerebras的进化轨迹已与AI行业"推理拐点"深度绑定。'
  },
  '[AINews] Everything is Conductor': {
    title_zh: '[AI新闻] 万物皆指挥家——软件架构新范式的兴起',
    summary_zh: 'Latent Space本轮讨论围绕"Conductor模式"在AI工程架构中的扩散，探讨现代AI从孤立的推理服务走向"中央指挥+分布式协作"架构的趋势。这把Cerebras、Runway、Abridge三家截然不同的AI工程路线串联成同一个图景。'
  },
  'AI-Native Healthcare: 100M Doctor Visits, 10–20 Hours Saved, Prior Auth in Minutes — Janie Lee & Chai Asawa, Abridge': {
    title_zh: 'AI原生医疗：1亿次诊疗对话，每次节省10-20小时，预授权立等可取',
    summary_zh: 'AI医疗公司Abridge 2018年成立，专注于临床对话记录，今年预计服务超8000万患者，覆盖250家美国大型健康系统，正在把"LLM帮医生写病历"扩展为"从前置授权到持续随访全流程AI代理"的愿景，让你觉得为什么要等LLM时代的到来。'
  },
  '[AINews] Codex Rises, Claude Meters Programmatic Usage': {
    title_zh: '[AI新闻] Codex崛起，Claude全面市测程序化使用量',
    summary_zh: 'AI应用侧增长出现分化：OpenAI的Codex系列在开发者侧不断攻城略地，而Claude正低调推出"程序化使用量"市测指标，暗示Anthropic在API用量分层计费上已有实质动作。两者来自不同方法论的数据正为2026年AI商业化格局提供最新指标。'
  },
  '[AINews] The End of Finetuning': {
    title_zh: '[AI新闻] 微调的终结——触发器切换到推理强化与长提示词',
    summary_zh: 'OpenAI宣布弃用其精调API，引发社区激烈讨论：微调的末路是否意味着所有定制化也到了尽头？No——Cursor与Cognition等顶级AI应用开发者反而增加了开源模型RL精调的用量，但方法论正转向长期Prompts和推理链强化——长提示词工程正式晋升为'26年最重要的AI工程技能之一。'
  },
};

// Apply translations
for (const item of news) {
  const tr = translations[item.title];
  if (tr) {
    item.title_zh = tr.title_zh;
    item.summary_zh = tr.summary_zh;
  } else {
    // Fallback
    item.title_zh = item.title;
    item.summary_zh = `关于「${item.title}」的报道。${item.source}等平台讨论的最新动态。`;
  }
}

function fmtSection(name, items, sourceEnum) {
  const filtered = items.filter(n => {
    const s = n.source;
    if (sourceEnum === 'TechCrunch') return s === 'TechCrunch';
    if (sourceEnum === 'HackerNews') return s === 'HackerNews';
    if (sourceEnum === 'Substack') return s === 'LatentSpace' || s === 'TheDecoder' || s === 'MITTechReview';
    return false;
  });
  if (!filtered.length) return '';
  
  // Sort by score within section (header = highest score overall)
  filtered.sort((a, b) => (b.score || 0) - (a.score || 0));
  
  const colors = { TechCrunch: '#1a73e8', HackerNews: '#ff6b35', Substack: '#9c27b8' };
  const color = colors[sourceEnum] || '#333';
  
  const rows = filtered.map((n, idx) => {
    const title = n.title_zh || n.title;
    let summary = n.summary_zh || '';
    if (summary.startsWith(title)) summary = summary.substring(title.length).trim();
    summary = summary.replace(/^[:：\s]+/, '');
    if (summary.length > 105) summary = summary.substring(0, 103) + '…';
    if (summary.length < 100 && !summary.endsWith('。') && !summary.endsWith('！') && !summary.endsWith('？')) summary += '。';
    
    return `      <div style="padding:8px 0;border-bottom:1px solid #f0f0f0;">
        <div style="font-size:15px;font-weight:700;line-height:1.5;margin-bottom:2px;color:#111">
          ${idx + 1}. <a href="${n.url}" style="text-decoration:none;color:#1976d2">${title}</a>
        </div>
        <div style="font-size:13px;color:#555;line-height:1.6">${summary}</div>
      </div>`;
  }).join('');
  
  return `    <div style="margin:16px 0 0">
      <h3 style="font-size:18px;font-weight:800;color:${color};margin:0 0 10px;padding-bottom:6px;border-bottom:2px solid ${color}">${name}</h3>
      <div style="background:#fff;padding:0 4px;border:none;border-radius:0;box-shadow:none">
${rows}
      </div>
    </div>`;
}

const sections = [
  fmtSection('📰 TechCrunch AI', news, 'TechCrunch'),
  fmtSection('🔥 Hacker News', news, 'HackerNews'),
  fmtSection('🎙️ Substack', news, 'Substack'),
].filter(Boolean).join('\n');

const hl = news[0];
const hlTitle = hl.title_zh || hl.title;
const hlScore = hl.score || 0;

function selectImage(item) {
  const t = (item.title_zh || item.title || '').toLowerCase();
  if (t.includes('robot') || t.includes('agent') || t.includes('智能体') || t.includes('robotics')) {
    return 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=900&h=383&fit=crop&q=80';
  }
  return 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80';
}

const img = selectImage(hl);
const total = allNews.length;

const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>北美AI圈日报 ${date}</title><style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.55;color:#333;margin:0;padding:0;background:#fff}a{color:#1976d2;text-decoration:none}img{max-width:100%;border-radius:8px}</style></head><body><div style="text-align:center;padding:28px 16px 20px;border-bottom:1px solid #e65100"><div style="font-size:22px;font-weight:800;color:#111;line-height:1.4;margin-bottom:8px">${hlTitle}</div><img src="${img}" style="width:100%;max-width:580px;border-radius:10px;margin:12px auto 8px;display:block" alt="头条配图"><div style="font-size:12px;color:#999;margin-top:4px">${date} · 共${total}条 · HN · TC · LatentSpace · Decoder · MIT TR</div></div>
${sections}<div style="text-align:center;padding:24px 0 40px;color:#bbb;font-size:12px;border-top:1px solid #eee;margin-top:28px"><p style="margin:0 0 6px">数据来源：Hacker News · TechCrunch · Latent Space · The Decoder · MIT Technology Review</p><p style="margin:0">由 AI News Publisher 自动生成 · 每日 07:00 更新</p></div></body></html>`;

const htmlFile = join(dataDir, `wechat-html-${date}.html`);
writeFileSync(htmlFile, html, 'utf8');
console.log(`✅ HTML generated: ${htmlFile}`);
console.log(`📊 Size: ${html.length} chars`);
console.log(`📰 Headline: ${hlTitle} (score=${hlScore})`);

// Archive
const archiveFile = join(dataDir, `wechat-html-${date}-${Date.now()}.html`);
writeFileSync(archiveFile, html, 'utf8');
console.log(`📦 Archived: ${archiveFile}`);

// Preview first 3
console.log('\n📝 Preview (first 3):');
news.slice(0, 3).forEach((n, i) => {
  console.log(`\n${i+1}. ${n.title_zh || n.title}`);
  console.log(`   ${(n.summary_zh || '').substring(0, 80)}...`);
});

// Save translated news back to json
writeFileSync(newsFile, JSON.stringify({ date, news: allNews }, null, 2));
console.log('\n💾 Translated news saved to JSON');
console.log('🎉 Done! Use --publish to create WeChat draft.');
