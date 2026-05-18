#!/usr/bin/env python3
"""
AI News Publisher - 2026-05-16
Loads today's raw news, applies translations, generates WeChat HTML.
"""
import json, time
from pathlib import Path

DATA  = Path("/root/.openclaw/workspace/skills/ai-news-publisher/data")
DATE  = "2026-05-16"

# ── Translations ──────────────────────────────────────────────────────────
# map original title → (zh_title, zh_summary)
TRANS = {
    "UK sovereign LLM inference": (
        "英国主权大模型推理：AI自主可控的技术路径",
        "Relax.ai 推出了 UK Sovereign Inference 项目，探讨在美国大模型依赖受限背景下如何自主训练和部署 LLM。蓝图涵盖硬件选型、模型蒸馏与合规审查，是技术去中心化的最新落地方案。"
    ),
    "Show HN: We built a narrative analysis engine for fiction writers": (
        "Show HN：为小说作家打造角色叙事分析器",
        "两位开发者为小说作家打造了一款情绪叙事自动识别引擎，读取手稿后依次标注各角色情绪曲线与叙事节奏，并生成心理弧光可视化、人物关系追踪和冲突密度曲线，让作家从数据视角审视人物塑造。"
    ),
    "Show HN: Emergence World: World building as a way to evaluate LLMs": (
        "Show HN：Emergence World——用世界观构建测试 LLM 智能",
        "Emergence World 把《开放世界中的世界观构建》作为 LLM 能力测试面，要求模型在开放世界游戏中形成自洽的世界规则与剧情，从康威生命游戏扩展出发评估多步推理与长期规划能力，替代传统要点式的静态评测框架。"
    ),
    "Learning, Fast and Slow: Towards LLMs That Adapt Continually": (
        "学习，快与慢：让大模型持续自适应的愿景",
        "GEPA 团队提出 Fast-Slow Training 框架，以提示词层为快权重、网络参数为慢权重交替训练，在数学和代码推理基准上全面超越仅调参的方案，以三倍少步数接近 RL 水平，同时保留持续学习新任务不丢失 plasticity 的能力。"
    ),
    "There's a $50B company hiding inside Salesforce": (
        "Salesforce 内部藏着一家 500 亿美元的公司",
        "Hacker News 帖子爆料 Salesforce 内部藏有一家估约 500 亿美元的业务单元，触发广泛讨论。帖子串联了巨型 SaaS 并购内幕与巨头产品组合管理的内部视角，是最近 AI 行业并购战局热潮背景下的珍贵一瞥。"
    ),
    "The OpenAI trial wraps up, and the Musk founder machine keeps spinning": (
        "OpenAI 庭审结束，马斯克的创始机器仍在高速运转",
        "OpenAI 与马斯克的法律博弈方兴未艾，马斯克却借 AI 叙事把创始神话一路演到硅谷聚光灯正中央。TechCrunch 播客从法律、产业和个人叙事三重维度复盘，认为 AI 黄金十年正把技术创始人的戏剧化叙事推向新高峰。"
    ),
    "Silicon Valley's vacationland needs a new energy provider just as AI is driving prices up": (
        "硅谷度假胜地急需新电力供应商，AI 用热潮正推高电价",
        "加州 Monterey 半岛主要依赖单一电力来源，夏季停电风险居高不下。AI 数据中心庞大用电浮出水面并推高当地电价，度假区不得不在高处电价下紧急寻找新供电商——揭示 AI 扩张与电网滞后的结构性矛盾正从硅谷向外扩散。"
    ),
    "OpenAI launches ChatGPT for personal finance, will let you connect bank accounts": (
        "OpenAI 发布 ChatGPT 个人理财功能，可对接银行账户",
        "ChatGPT Pro 用户现可接入 12000+ 家金融机构，自动汇总净资产、月度支出和未来现金流预测。已有上亿次金融咨询在 ChatGPT 内发生，新功能借助 GPT-5.5 推理增强直接让对话变资产负债表分析。"
    ),
    "Runway started by helping filmmakers -- now it wants to beat Google at AI": (
        "Runway 从协助影人起步——如今正面挑战 Google AI",
        "Runway 创始人联合 CEO Germanidis 认为语言范式 AI 有本质局限，下一代智能将从视频和世界模型出发，直接观察物理世界。最新 Gen-4.5 己获多数好莱坞制作团队采用，Runway 下一步赌注在于让 AI 从描述画面跃迁至理解并创造物理世界本身。"
    ),
    "Osaurus brings both local and cloud AI models to your Mac": (
        "Osaurus 让本地与云端 AI 模型在 Mac 上统一运行",
        "OSaur I<source>'面向 Mac 打造统一 AI 平台，16GB 统一内存即可本地跑 SmolLM3，复杂任务自动切换云端大模型，无缝衔接 Apple Silicon 本地推理与云端通用模型能力，大大降低在无 GPU Mac 上用 AI 的门槛。"
    ),
    "[AINews] Cerebras' $60B IPO: Slowly, then All at Once": (
        "[AI新闻] Cerebras：600 亿美元 IPO，慢跑后全力冲刺上市",
        "AI 芯片明星公司 Cerebras IPO 首日收于 280 美元，市值达 600 亿美元。与 OpenAI 签署大规模部署协议后 TSMC 晶圆产能正成 2028 年前持续瓶颈，印证 AI 推理拐点下算力军备竞赛已全面升级。"
    ),
    "[AINews] Everything is Conductor": (
        "[AI新闻] 万物皆指挥台——软件架构从单点向分布演进的寓言",
        "本轮讨论围绕指挥台模式在 AI 工程架构中的扩散展开。Cerebras 在卖芯片，Runway 在做世界模型，Abridge 在执行业务 AI 代理——三家技术路径看似无关，在指挥台架构的视角下已有了共同的方法论语言。"
    ),
    "AI-Native Healthcare: 100M Doctor Visits, 10-20 Hours Saved, Prior Auth in Minutes -- Janie Lee & Chai Asawa, Abridge": (
        "AI 原生医疗：一亿诊疗对话，单次节省 10-20 工时，前置授权立等可取",
        "Abridge 2018 年成立，原本做病历记录辅助，今年预计服务超 8000 万患者，覆盖 250 家美国大型医疗体系。现在它正把工作流从前置记录扩展到全流程 AI 代理，成为医疗 AI 大觉醒最具说服力的案例之一。"
    ),
    "[AINews] Codex Rises, Claude Meters Programmatic Usage": (
        "[AI新闻] Codex 加速崛起，Claude 计量程序化 API 调用量",
        "OpenAI Codex 系列在开发者侧攻城略地，Claude 则悄然推出按程序调用次数计费。Audit 数据显示 Anthropic 在企业侧有着深厚的开发者生态存款，API 用量分层正式进入实测阶段，2026 AI 商业地图两份数据给足了分析师考题。"
    ),
    "[AINews] The End of Finetuning": (
        "[AI新闻] 微调的终结——长提示词工程成为 2026 年新核心技能",
        "OpenAI 弃用精调 API 引发社区热议，但 Cursor、Cognition 等顶级 AI 开发商反而增开开源精调——只是路径从端到端权重更新换成长提示词工程加推理强化。AI 工程核心技能结构正在发生迁移，2026 年大概率要被载入提示词工程史册。"
    ),
}

# ── Load news ─────────────────────────────────────────────────────────────
raw   = json.loads((DATA / f"news-{DATE}.json").read_text())
all_n = raw["news"]
all_n.sort(key=lambda x: x.get("score", 0), reverse=True)
top15 = all_n[:15]

for n in top15:
    key = n["title"]
    tr = TRANS.get(key)
    if tr:
        n["title_zh"]    = tr[0]
        n["summary_zh"]  = tr[1]
    else:
        n["title_zh"]   = key
        n["summary_zh"] = f"关于「{key}」的报道。（{n['source']}）"

# ── Helpers ───────────────────────────────────────────────────────────────
def smart_trunc(s, mx=105):
    if len(s) <= mx: return s
    for punc in ("。", "！", "?", "？", "；"):
        pos = s[:mx].rfind(punc)
        if pos > 30:
            return s[:pos + 1]
    return s[:mx - 3] + "…"

def section(name, items, color, sources):
    fi = [n for n in items if n["source"] in sources]
    if not fi: return ""
    fi.sort(key=lambda x: x.get("score", 0), reverse=True)
    rows = []
    for i, n in enumerate(fi):
        t = n["title_zh"] or n["title"]
        s = n["summary_zh"] or ""
        if s.startswith(t):
            s = s[len(t):].strip()
        s = s.lstrip(":： —-")
        s = smart_trunc(s)
        rows.append(
            '      <div style="padding:8px 0;border-bottom:1px solid #f0f0f0;">'
            '<div style="font-size:15px;font-weight:700;line-height:1.5;margin-bottom:2px;color:#111">'
            f'{i+1}. <a href="{n["url"]}" style="text-decoration:none;color:#1976d2">{t}</a>'
            '</div><div style="font-size:13px;color:#555;line-height:1.6">'
            f'{s}</div></div>'
        )
    return (
        '    <div style="margin:16px 0 0">'
        f'<h3 style="font-size:18px;font-weight:800;color:{color};margin:0 0 10px;'
        f'padding-bottom:6px;border-bottom:2px solid {color}">{name}</h3>'
        '  <div style="padding:0 4px">\n' + "\n".join(rows) + "\n</div>\n    </div>"
    )

def img_for(item):
    t = (item.get("title_zh","") or item.get("title","")).lower()
    for kw in ("robot","agent","智能体","robotics","humanoid","colonoscopy","视频","film"):
        if kw in t:
            return "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=900&h=383&fit=crop&q=80"
    return "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80"

# ── Build HTML ─────────────────────────────────────────────────────────────
blocks = "\n".join(filter(bool, [
    section("TechCrunch AI",   top15, "#1a73e8", ["TechCrunch"]),
    section("Hacker News",     top15, "#ff6b35", ["HackerNews"]),
    section("Substack",        top15, "#9c27b8", ["LatentSpace","TheDecoder","MITTechReview"]),
    # Leftover sources (if any)
]))

hl      = top15[0]
hl_title = hl["title_zh"] or hl["title"]
hl_score = hl.get("score", 0)
total   = len(all_n)

img = img_for(hl)

html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>北美AI圈日报 {DATE}</title><style>body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.55;color:#333;margin:0;padding:0;background:#fff}}a{{color:#1976d2;text-decoration:none}}img{{max-width:100%;border-radius:8px}}</style></head><body><div style="text-align:center;padding:28px 16px 20px;border-bottom:1px solid #e65100"><div style="font-size:22px;font-weight:800;color:#111;line-height:1.4;margin-bottom:8px">{hl_title}</div><img src="{img}" style="width:100%;max-width:580px;border-radius:10px;margin:12px auto 8px;display:block" alt="header"><div style="font-size:12px;color:#999;margin-top:4px">{DATE} · 共{total}条 · Hacker News · TechCrunch · Latent Space · The Decoder · MIT TR</div></div>
{blocks}<div style="text-align:center;padding:24px 0 40px;color:#bbb;font-size:12px;border-top:1px solid #eee;margin-top:28px"><p style="margin:0 0 6px">数据来源：Hacker News · TechCrunch · Latent Space · The Decoder · MIT Technology Review</p><p style="margin:0">由 AI News Publisher 自动生成 · 每日 07:00 更新</p></div></body></html>"""

# ── Save ──────────────────────────────────────────────────────────────────
(DATA / f"wechat-html-{DATE}.html").write_text(html, "utf8")
(DATA / f"wechat-html-{DATE}-{int(time.time()*1000)}.html").write_text(html, "utf8")
(DATA / f"news-{DATE}.json").write_text(json.dumps({"date": DATE, "news": all_n}, ensure_ascii=False, indent=2), "utf8")

print(f"✅ HTML 生成  {DATE}  ({len(html):,} chars)")
print(f"📰 头条: {hl_title}  (score={hl_score})")
print(f"📊 选稿: {len(top15)} 条 / 来源共 {total} 条")
print("\n📝 前 3 预览:")
for i, n in enumerate(top15[:3]):
    s = (n.get("summary_zh","") or "")[:80]
    print(f"\n[{i+1}] {n['title_zh']}")
    print(f"    {s}…")
print("\n🎉 完成！用 --publish 可一键生成公众号草稿。")
