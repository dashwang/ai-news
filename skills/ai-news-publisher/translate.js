import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const dataDir = '/root/.openclaw/workspace/skills/ai-news-publisher/data';
const newsFile = join(dataDir, 'news-2026-04-29.json');
const { news } = JSON.parse(readFileSync(newsFile, 'utf8'));

const dict = {
  "Yann LeCun: LLMs Are Nearing the End, but Better AI Is Coming (2025)": "Yann LeCun：大语言模型将触及天花板，但更优的 AI 正在路上（2025）",
  "World's First conversational AI skills assessment": "全球首个会话式 AI 技能评估系统",
  "Show HN: Knowerage – code coverage for LLM analysis": "Show HN：Knowerage — LLM 代码覆盖率分析工具",
  "Amazon is already offering new OpenAI products on AWS": "亚马逊 AWS 已开始提供 OpenAI 最新产品",
  "Amazon launches an AI-powered audio Q&A experience on product pages": "亚马逊推出 AI 语音问答：商品页面可直接语音对话",
  "Google expands Pentagon's access to its AI after Anthropic's refusal": "Google 扩大五角大楼 AI 访问权限，Anthropic 曾拒绝合作",
  "Import AI 453: Breaking AI agents; MirrorCode; and ten views on gradual disempowerment": "Import AI 453：AI 代理突破、MirrorCode 与渐进式削弱的十个观点",
  "Import AI 451: Political superintelligence; Google's society of minds, and a robot drummer": "Import AI 451：政治超级智能、Google 心灵社会与机器鼓手",
};

const summaries = {
  "Yann LeCun: LLMs Are Nearing the End, but Better AI Is Coming (2025)": "Yann LeCun 访谈：LLM 即将触及天花板，但更好的 AI 正在路上（2025 展望）",
  "World's First conversational AI skills assessment": "全球首个会话式 AI 技能评估系统发布，用于衡量 AI 代理在对话中的能力表现。",
  "Show HN: Knowerage – code coverage for LLM analysis": "Knowerage 是一个开源工具，用于分析 LLM 生成的代码覆盖率，帮助开发者评估 AI 编程质量。",
  "Amazon is already offering new OpenAI products on AWS": "Amazon AWS Bedrock 平台新增 OpenAI 最新模型及 Codex 代码编写服务，扩大与 OpenAI 的合作范围。",
  "Amazon launches an AI-powered audio Q&A experience on product pages": "亚马逊在商品详情页新增 AI 语音问答功能，消费者可通过语音提问了解产品细节，是电商 AI 交互的新尝试。",
  "Google expands Pentagon's access to its AI after Anthropic's refusal": "在 Anthropic 拒绝向五角大楼提供无限制访问后，Google 决定扩大其 AI 系统的访问权限，可用于分类网络上的所有合法用途。",
  "Import AI 453: Breaking AI agents; MirrorCode; and ten views on gradual disempowerment": "Import AI 第 453 期：探讨 AI agent 的最新突破、MirrorCode 工具，以及关于 AI 渐进式权力削弱的十个不同视角。",
  "Import AI 451: Political superintelligence; Google's society of minds, and a robot drummer": "Import AI 第 451 期：讨论政治领域的超级智能、Google 的 \"心灵社会\" 概念，以及一个能够打鼓的机器人项目。",
};

for (const item of news) {
  item.title_zh = dict[item.title] || item.title;
  item.summary_zh = summaries[item.title] || item.title_zh.substring(0, 120);
}

writeFileSync(newsFile, JSON.stringify({ date: '2026-04-29', news }, null, 2));
console.log('✅ Translation complete');
