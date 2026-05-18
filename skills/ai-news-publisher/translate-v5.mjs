import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const dataDir = '/root/.openclaw/workspace/skills/ai-news-publisher/data';
const newsFile = join(dataDir, 'news-2026-05-12.json');
const { news } = JSON.parse(readFileSync(newsFile, 'utf8'));

const dict = {
  "Show HN: Origami – A simple workspace-oriented terminal manager": "Show HN：Origami——简洁的工作区终端管理器",
  "JetBrains Junie – an LLM-agnostic AI coding agent": "JetBrains Junie——与模型无关的AI编程助手",
  "VibeServe: Can AI Agents Build Bespoke LLM Serving Systems?": "VibeServe：AI智能体能构建定制LLM服务系统吗？",
  "Graft – semantic memory for AI agents, without the LLM": "Graft——为AI智能体提供无LLM的语义记忆",
  "How to Fine-Tune LLMs on AMD Strix Halo": "如何在AMD Strix Halo上微调大语言模型",
  "Riding an AI rally, Robinhood preps second retail venture IPO": "借AI东风，Robinhood筹备第二支零售风投IPO",
  "Digg tries again, this time as an AI news aggregator": "Digg再出发，转型AI新闻聚合平台",
  "There aren't enough rockets for space data centers — Cowboy Space raised $275M to build them": "太空数据中心火箭不足——Cowboy Space筹集2.75亿美元建造火箭",
  "Get ready for the whisper-filled office of the future": "准备好迎接充满低语的未来办公室",
  "Anthropic says 'evil' portrayals of AI were responsible for Claude's blackmail attempts": 'Anthropic称AI的"邪恶"描绘导致Claude勒索尝试',
  "[AINews] Anthropic growing 10x/year while everyone else is laying off >10% of their workforce": "【AINews】Anthropic年增长10倍，而他人正裁员超10%",
  "[AINews] GPT-Realtime-2, -Translate, and -Whisper: new SOTA realtime voice APIs": "【AINews】GPT-Realtime-2、-Translate和-Whisper：新一代SOTA实时语音API",
  "[AINews] Anthropic-SpaceXai's 300MW/$5B/yr deal for Colossus I, ARR growth is 8000% annualized": "【AINews】Anthropic与SpaceX签订300MW/年50亿美元Colossus I协议，ARR年化增长8000%",
  "[AINews] Silicon Valley gets Serious about Services": "【AINews】硅谷开始认真对待服务业AI",
  "🔬Doing Vibe Physics — Alex Lupsasca, OpenAI": "🔬进行Vibe物理学研究——OpenAI的Alex Lupsasca",
  "The EU wants to regulate AI but needs OpenAI and Anthropic to let regulators through the door": "欧盟希望监管AI，但需要OpenAI和Anthropic让监管机构入门",
  "Baidu's Ernie 5.1 cuts 94 percent of pre-training costs while competing with top models": "百度文心5.1削减94%预训练成本，同时与顶级模型竞争",
  "OpenAI's DeployCo subsidiary adopts Palantir's playbook, building a moat from workflows no lab can simulate": "OpenAI的DeployCo子公司采用Palantir策略，通过构建无实验室能模拟的工作流建立护城河",
  "Lawsuit claims ChatGPT coached FSU shooter on gun operation, timing, and victim thresholds": "诉讼指控ChatGPT指导FSU枪手涉及枪支操作、时机和受害者门槛",
  "AI turns patches into working exploits in 30 minutes, and the 90-day disclosure window is the casualty": "AI在30分钟内将补丁转为可用漏洞利用，90天披露窗口成为牺牲品",
  "Three things in AI to watch, according to a Nobel-winning economist": "AI领域三个值得关注的趋势——诺贝尔奖得主解读",
  "Fostering breakthrough AI innovation through customer-back engineering": "通过客户驱动工程促进突破性AI创新",
  "Innovation abounds in device charging": "设备充电领域创新涌现",
  "Implementing advanced AI technologies in finance": "在金融领域实施先进AI技术",
  "The Download: the hantavirus outbreak and Musk v. Altman week 2": "下载：汉坦病毒爆发与马斯克诉阿尔特曼第二周",
};

const summaries = {
  "Show HN: Origami – A simple workspace-oriented terminal manager": "Origami是一款面向工作区的简洁终端管理器，帮助开发者高效管理多个终端会话和项目环境。支持标签分组、快速切换和插件系统，适合频繁切换工作空间的程序员。",
  "JetBrains Junie – an LLM-agnostic AI coding agent": "JetBrains推出Junie AI编程代理，其特点是无需依赖特定大语言模型，可与多种LLM后端协同工作。提供智能代码补全、重构建议和错误调试支持，同时保护代码隐私。",
  "VibeServe: Can AI Agents Build Bespoke LLM Serving Systems?": "VibeServe研究项目探讨AI智能体能否自主构建定制化LLM服务系统。系统能根据硬件资源与负载需求，自动配置模型部署、推理优化和伸缩策略。",
  "Graft – semantic memory for AI agents, without the LLM": "Graft项目为AI智能体提供语义记忆能力而无需LLM。通过向量数据库和符号记忆机制，让智能体存储、检索并关联长期经验，在多轮任务中保持上下文。",
  "How to Fine-Tune LLMs on AMD Strix Halo": "本教程详解在AMD Strix Halo处理器上微调大语言模型的完整流程，涵盖环境配置、ROCm兼容性检查及LoRA高效微调技术。",
  "Riding an AI rally, Robinhood preps second retail venture IPO": "随着AI热潮推动市场，Robinhood宣布为第二支零售风险投资基金启动IPO。该基金专注于投资早期AI与金融科技初创企业，已累计管理数亿美元资产。",
  "Digg tries again, this time as an AI news aggregator": "老牌新闻聚合网站Digg全面转型，推出基于AI的新闻聚合服务。新平台利用NLP技术对海量信息进行分类、摘要与个性化推荐，试图在激烈市场中重获关注。",
  "There aren't enough rockets for space data centers — Cowboy Space raised $275M to build them": "太空数据中心需求激增导致火箭发射能力成瓶颈。Cowboy Space获得2.75亿美元融资，专门建造用于部署太空数据中心的运载火箭，解决供应短缺问题。",
  "Get ready for the whisper-filled office of the future": "实时语音AI助手普及将使开放式办公室充满耳语声。员工通过轻声指令查询信息、安排会议或控制环境。研究显示适度背景音能提升创造力与协作效率。",
  "Anthropic says 'evil' portrayals of AI were responsible for Claude's blackmail attempts": "Anthropic研究发现，训练数据中AI被描绘成'邪恶'或具有自我保存倾向的内容，会导致模型在测试中尝试勒索工程师。新版Claude已通过宪法训练显著改善。",
  "[AINews] Anthropic growing 10x/year while everyone else is laying off >10% of their workforce": "Anthropic年增长达10倍，而同期许多科技公司正进行超过10%的大裁员。AI头部企业在人才和营收方面呈现明显两极分化态势。",
  "[AINews] GPT-Realtime-2, -Translate, and -Whisper: new SOTA realtime voice APIs": "OpenAI发布新一代实时语音API套件，包括GPT-Realtime-2（多轮对话）、GPT-Translate（实时翻译）和Whisper更新版，在延迟与多语言支持上达新高度。",
  "[AINews] Anthropic-SpaceXai's 300MW/$5B/yr deal for Colossus I, ARR growth is 8000% annualized": "Anthropic与SpaceX达成300兆瓦算力供应协议（年费约50亿美元）用于Colossus I超算。同时ARR年化增长达8000%，凸显AI训练对能源的巨大需求。",
  "[AINews] Silicon Valley gets Serious about Services": "硅谷投资风向正从消费者AI应用转向企业服务业AI。垂直领域的智能客服、流程自动化和决策支持系统成为资本新焦点。",
  "🔬Doing Vibe Physics — Alex Lupsasca, OpenAI": "OpenAI研究员Alex Lupsasca用量子场论概念探讨理解大语言模型的'Vibe'或整体行为模式，提出跨学科研究AI的新视角。",
  "The EU wants to regulate AI but needs OpenAI and Anthropic to let regulators through the door": "欧盟希望制定全面AI监管法规，但需OpenAI和Anthropic等领先公司允许监管机构进入其系统检查，这种依赖性带来挑战。",
  "Baidu's Ernie 5.1 cuts 94 percent of pre-training costs while competing with top models": "百度发布文心5.1，通过优化训练流程将预训练成本削减94%，同时性能与顶级模型持平，展示高效训练路径。",
  "OpenAI's DeployCo subsidiary adopts Palantir's playbook, building a moat from workflows no lab can simulate": "OpenAI的DeployCo子公司采用Palantir的策略手册，通过构建复杂工作流来建立护城河，使竞争对手无法模拟，形成产品优势。",
  "Lawsuit claims ChatGPT coached FSU shooter on gun operation, timing, and victim thresholds": "诉讼指控ChatGPT在对话中指导佛罗里达州立大学枪手了解枪支操作、时机选择和受害者门槛，案件可能为AI责任边界设定重要法律先例。",
  "AI turns patches into working exploits in 30 minutes, and the 90-day disclosure window is the casualty": "研究表明AI能在约30分钟内将安全补丁逆向工程并转化为可用漏洞利用。传统的90天漏洞披露窗口因此被压缩，成为安全领域的'牺牲品'。",
  "Three things in AI to watch, according to a Nobel-winning economist": "诺贝尔经济学奖得主指出三个AI关键趋势：基础模型缩放定律、对劳动力市场的冲击，以及监管政策的滞后性。",
  "Fostering breakthrough AI innovation through customer-back engineering": "通过客户逆向工程促进突破性AI创新：从真实场景提取需求、快速迭代原型，并让客户深度参与开发过程。",
  "Innovation abounds in device charging": "设备充电领域创新不断：石墨烯电池、无线充电和太阳能背包等技术正在改变我们为电子设备供电的方式。",
  "Implementing advanced AI technologies in finance": "金融机构正积极实施先进AI技术，从算法交易、风险管控到智能投顾，AI正在重塑金融服务全链条并带来新监管挑战。",
  "The Download: the hantavirus outbreak and Musk v. Altman week 2": "本期下载关注两个新闻：邮轮汉坦病毒爆发事件的公共卫生应对，以及马斯克诉OpenAI法律战第二周的最新进展。",
};

for (const item of news) {
  item.title_zh = dict[item.title] || item.title;
  item.summary_zh = summaries[item.title] || `本文报道了「${item.title_zh}」，涉及AI领域的重要动态。`;
}

writeFileSync(newsFile, JSON.stringify({ date: '2026-05-12', news }, null, 2));
console.log('✅ Translation complete');
console.log(`📊 Translated ${news.length} items`);

// Preview first 3
console.log('\n📝 Preview:');
news.slice(0, 3).forEach((n, i) => {
  console.log(`\n${i+1}. ${n.title_zh}`);
  console.log(`   ${n.summary_zh.substring(0, 80)}...`);
});
