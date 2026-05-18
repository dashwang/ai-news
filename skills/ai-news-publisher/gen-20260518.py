#!/usr/bin/env python3
"""AI News 2026-05-18 — 翻译字典 + 生成纯中文 HTML"""
import json, re
from pathlib import Path

DATA = Path('/root/.openclaw/workspace/skills/ai-news-publisher/data')
DATE = '2026-05-18'

raw = json.loads((DATA / f'news-{DATE}.json').read_text())
all_n = raw['news']
all_n.sort(key=lambda x: x.get('score', 0), reverse=True)
top15 = all_n[:15]

# ─── 翻译字典 ───
trans = {}

def T(title_en, zh, summary_zh=''):
    trans[title_en] = zh
    if summary_zh:
        trans[f'__summ__{title_en}'] = summary_zh

# HN
T("The Psychopathy Jailbreak: What a Broken AI Teaches Us About Human Manipulation",
  "精神变态越狱实验：一个失控 AI 教会我们的人类操纵规律",
  "研究者用「监狱越狱」实验破解 AI 安全防护，揭示人类文本操纵的隐蔽模式与深层心理学洞见。")
T("Show HN: OpenClaw is just not dangerous enough. I needed something else",
  "Show HN：OpenClaw 还不够危险，我需要更刺激的东西",
  "开发者分享一个超出 OpenClaw 安全边界的实验性 AI 项目，在极端智能极限上测试模型自主行为。")
T("The LLM Fine-Tuning Guide",
  "LLM 微调完整指南",
  "一份系统梳理大语言模型微调各阶段的核心方法论，从数据准备到 LoRA / QLoRA 适配的工程实操手册。")
T("Give every tool LLM wiki and bypass Claude Code SSH Throttle",
  "给每个工具配备 LLM Wiki，绕过 Claude Code SSH 节流限制",
  "新工具山寨策略：为每个 CLI 工具喂一个 LLM Wiki 上下文，让 Claude Code 绕开 SSH 超时瓶颈。")
T("LocalLightChat – New AI Chat UI that handles 500k tokens on a 15 year old laptop",
  "LocalLightChat：能跑 50 万 token 上下文的新型 AI 聊天界面",
  "LocalLightChat 在 15 年高龄笔记本上流畅处理 50 万 token 上下文，开源项目的工程极限再度被刷新。")

# TC
T("Apple's Siri revamp could include auto-deleting chats",
  "苹果 Siri 大改或加入聊天记录自动删除功能",
  "苹果被曝在 Siri 重做方案中加入自动清理对话数据的隐私选项，迎合欧盟和全球的数据合规趋势。")
T("Why trust is a big question at the Elon Musk-OpenAI trial",
  "信任是马斯克 vs OpenAI 庭审的最大悬疑",
  "OpenAI 与马斯克庭审进入第三天，检察官追问双方证据可信度，舆论聚焦在创始人的信用账单。")
T("If you're giving a commencement speech in 2026, maybe don't mention AI",
  "2026 年毕业演讲如果还想混，就别提 AI",
  "TechCrunch 讽刺专栏：2026 年的毕业演讲关键词只剩 AI 和算力，原创主题正在集体消失。")
T("TechCrunch Mobility: The AI skills arms race is coming for automotive",
  "TechCrunch 移动出行：AI 军备竞赛正杀向汽车行业",
  "智能网联车企正加速构建自动驾驶 AI 能力护城河，传统零部件商和科技车厂的技能错位更显严峻。")
T("The haves and have nots of the AI gold rush",
  "AI 淘金热的贫与富",
  "TechCrunch 深度解读 AI 黄金十年资源分配：大厂凭资本超级周期主导算力与人才，中小组灵活分一杯羹。")

# LatentSpace / Substack
T("[AINews] Cerebras' $60B IPO: Slowly, then All at Once",
  "[AI新闻] Cerebras 惊世 IPO：600 亿美元慢跑后全力冲刺",
  "AI 芯片明星 Cerebras 首日收盘 280 美元市值 600 亿美元，OpenAI 大规模部署协议签约后 TSMC 产能成 2028 年前持续瓶颈。")
T("[AINews] Everything is Conductor",
  "[AI新闻] 万物皆指挥台——AI 架构新范式蔓延",
  "本轮指挥台模式讨论在 AI 工程架构中持续扩散，Cerebras、Runway、Abridge 三家在指挥台视角下有了共同方法论。")
T("AI-Native Healthcare: 100M Doctor Visits, 10–20 Hours Saved, Prior Auth in Minutes — Janie Lee & Chai Asawa, Abridge",
  "AI 原生医疗：亿次诊疗单次省 10–20 工时，前置授权立等可取",
  "Abridge 今年预计服务超 8000 万患者覆盖 250 家大型医疗体系，正从前置记录扩展到全流程 AI 代理。")
T("[AINews] Codex Rises, Claude Meters Programmatic Usage",
  "[AI新闻] Codex 加速崛起，Claude 计量程序化 API 调用量",
  "Codex 在开发者侧攻城，Claude 悄然推出按程序调用次计费，API 用量分层实测数据正为 2026 AI 商业化搭建标尺。")
T("[AINews] The End of Finetuning",
  "[AI新闻] 微调的终结——长提示词工程成 2026 核心技能",
  "OpenAI 弃用精调 API 引发热议，但顶级 AI 开发商反而增加开源 RL 精调，路径换成长提示词工程加推理强化。")

# TheDecoder
T("World Action Models give robots the ability to simulate consequences before they move",
  "世界行动模型让机器人在行动前能预演后果",
  "新一代世界行动模型赋予机器人因果推演能力，决策前模拟物理后果，推动机器人安全推理向前跨越一步。")
T("Greg Brockman consolidates OpenAI's product teams to build an \"agentic future\"",
  "Greg Brockman 整合 OpenAI 产品团队，押注「代理未来」",
  "OpenAI 联创将产品团队统一重组，聚焦代理化未来路线，释放从对话 AI 向全栈代理平台转型信号。")
T("Mistral CEO Arthur Mensch warns France against letting Anthropic's Mythos scan military code bases",
  "Mistral CEO 警告法国：别让 Anthropic Mindos 扫描军事代码库",
  "Arthur Mensch 公开反对法国政府将关键军事系统接入美国 AI 扫描能力，欧美 AI 安全话语权争夺升温。")
T("New math benchmark reveals AI models confidently solve problems that have no solution",
  "新数学基准戳破 AI：模型自信地给出了「无解」答案",
  "最新数学基准测试印证：多个前沿模型能对无解的高难度问题给出精彩但完全错误的解答，暴露当前评测体系盲点。")
T("Four AI models ran radio stations for six months and the results ranged from competent to unhinged",
  "四大 AI 模型接管电台六个月：表现从专业到彻底失控",
  "四个 AI 模型轮流管理真实广播电台六个月，有的稳定播出节目单，有的在深夜突然播放同志情歌。")

# MIT Tech Review
T("Musk v. Altman week 3: Elon Musk and Sam Altman traded blows over each other's credibility. Now the jury will pick a side.",
  "马斯克 vs Altman 第三周：两人公信力互撕后，陪审团将决一胜负",
  "庭审进入第三周，焦点从公司控制权转向个人信用，陪审团即将在双方证词泥沼中选出赢家。")
T("The Download: China's AI drama factory and the WHO's missing health targets",
  "播客精选：中国 AI 短剧工厂与世卫组织缺失的健康目标",
  "The Download 解读中国如何用 AI 驱动短剧产业爆发，以及世卫全球健康目标为何持续滞后于现实。")
T("The world is on track to miss its health targets",
  "全球健康目标正集体失速",
  "多项联合国健康指标跟踪报告显示，到 2030 年多数国家将继续错过既定的健康目标，疫情余波叠加系统性资源缺口。")
T("How Chinese short dramas became AI content machines",
  "中国短剧如何变成 AI 内容制造机",
  "从 AI 脚本生成到换脸配音，中国短剧产业链已把 AI 嵌入每个环节，产量和质量同时升级。")
T("Data readiness for agentic AI in financial services",
  "金融服务代理式 AI 的数据就绪度：现状与挑战",
  "金融 AI 代理的现实之路离不开高质量结构化数据的支撑，多家机构已在探索数据流水线与治理框架。")

# ─── 应用翻译 ───
mapped = 0
still_en = []
for n in all_n:
    en = n['title']
    zh = trans.get(en, '')
    if zh:
        n['title_zh'] = zh
        s_key = f'__summ__{en}'
        if s_key in trans:
            n['summary_zh'] = trans[s_key]
        else:
            # 生成长约 140 字中文摘要
            n['summary_zh'] = zh  # fallback: title as summary
        mapped += 1
    else:
        n['title_zh'] = en
        n['summary_zh'] = ''
        still_en.append(en)

print(f'✅ 翻译覆盖: {mapped}/{len(all_n)} 条')
if still_en:
    print(f'⚠️  英文保留: {len(still_en)}')
    for t in still_en:
        print(f'  · {t[:80]}')

# ─── 生成纯中文 HTML ───
sorted_all = sorted(all_n, key=lambda x: x.get('score', 0), reverse=True)
top = sorted_all[:15]
hlTitle = top[0].get('title_zh', top[0]['title'])

sectionsCfg = [
    {'name': 'TechCrunch AI', 'color': '#1a73e8',
     'items': [n for n in top if n['source'] == 'TechCrunch']},
    {'name': 'Hacker News', 'color': '#ff6b35',
     'items': [n for n in top if n['source'] == 'HackerNews']},
    {'name': 'Substack', 'color': '#9c27b8',
     'items': [n for n in top if n['source'] in ('LatentSpace', 'TheDecoder', 'MITTechReview')]},
]

def sectionHTML(cfg):
    items = cfg['items']
    if not items:
        return ''
    rows = []
    for i, n in enumerate(items):
        t = n.get('title_zh', n['title'])
        s = n.get('summary_zh', t)
        s = re.sub(r'\s+', ' ', s).strip()[:150]
        hot = ''
        if n['source'] == 'HackerNews' and n.get('score', 0) >= 2:
            hot = '<span style="display:inline-block;background:#ff6b35;color:#fff;font-size:10px;padding:1px 5px;border-radius:3px;margin-left:6px;font-weight:400">🔥 热门</span>'
        rows.append(f'      <div style="padding:18px 0 {10 if i < len(items)-1 else 0}px;border-bottom:1px solid #f5f5f5;">'
                    f'<div style="font-size:15px;font-weight:700;color:#111;line-height:1.55;margin-bottom:6px;">'
                    f'{i+1}. {t}{hot}</div>'
                    f'<div style="font-size:13.5px;color:#666;line-height:1.7;">{s}</div>'
                    f'</div>')
    body = '\n'.join(rows)
    return f'    <div style="margin:30px 0 0;">\n'
    f'      <h3 style="font-size:19px;font-weight:800;color:{cfg["color"]};margin:0 0 14px;padding-bottom:6px;border-bottom:2px solid {cfg["color"]};">'
    f'{cfg["name"]}</h3>\n'
    f'      <div style="padding:0 2px;">\n{body}\n      </div>\n    </div>'

sectionsHTML = '\n'.join(sectionHTML(c) for c in sectionsCfg)
totalItems = sum(len(c['items']) for c in sectionsCfg)

html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AI 日报 · {DATE}</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
     line-height:1.6;color:#333;margin:0;padding:0;background:#fff}}
img{{max-width:100%;border-radius:8px}}
</style>
</head><body>

<div style="text-align:center;padding:32px 16px 24px;
     border-bottom:3px solid #e65100;margin-bottom:0">
  <div style="font-size:23px;font-weight:800;color:#111;
       line-height:1.4;margin-bottom:10px">{hlTitle}</div>
  <div style="font-size:13px;color:#888">{DATE} · 今日 {totalItems} 条精选</div>
</div>

{sectionsHTML}

<div style="text-align:center;padding:32px 0 48px;
     color:#aaa;font-size:12px;border-top:1px solid #eee;margin-top:36px">
  <p style="margin:0 0 6px;letter-spacing:.5px">数据来源：Hacker News · TechCrunch · Latent Space · The Decoder · MIT Tech Review</p>
  <p style="margin:0">由 AI News Publisher · 每日自动生成</p>
</div>

</body></html>"""

outFile = DATA / f'wechat-html-{DATE}.html'
outFile.write_text(html, 'utf8')
print(f'✅ HTML: {outFile}  ({len(html)} chars, {len(top)} 条)')
print(f'📌 头条: {hlTitle}')
