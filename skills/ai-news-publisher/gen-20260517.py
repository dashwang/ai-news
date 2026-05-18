#!/usr/bin/env python3
"""AI News Publisher - 2026-05-17"""
import json, time
from pathlib import Path

DATA = Path('/root/.openclaw/workspace/skills/ai-news-publisher/data')
DATE = '2026-05-17'

raw   = json.loads((DATA / f'news-{DATE}.json').read_text())
all_n = raw['news']
all_n.sort(key=lambda x: x.get('score',0), reverse=True)
top15 = all_n[:15]

def get_trans(title, source):
    h = title.lower()
    if 'offline voice to text' in h and 'keyboard' in h:
        return ('Show HN：离线语音转文字与 AI 键盘', '开发者推出离线语音输入与 AI 键盘概念，在无网络下实现语音转文字并与 AI 键盘无缝集成，主打隐私保护和离线可用。')
    if 'benchmark for local llm inference' in h:
        return ('Show HN：本地 LLM 推理与 GPU/CPU XGBoost 训练基准', '开源基准工具同时测量本地 LLM 推理延迟和传统机器学习训练吞吐量，本地 AI 开发者可快速对照不同硬件性能。')
    if 'frosthyon' in h:
        return ('Frosthyon：面向 3D 与通用工作流的 AI 助手', 'Frosthyon 是针对 3D 建模与通用工作流的新一代 AI 助手，统一建模、渲染、文本处理与代码编写，强调跨工具上下文感知。')
    if 'what we should be afraid of in ai' in h:
        return ('AI 面前我们该怕什么？（2021 重思）', '回看 2021 年 AI 风险讨论，对照当前大模型现状梳理：安全对齐失败、权力集中、系统价值观错位——今日仍然有回响。')
    if 'stera' in h and 'spatial' in h:
        return ('Stera：用 iPhone 采集空间数据训练世界模型的开放平台', '开源项目 Stera 利用 iPhone 传感器采集空间数据，为物理 AI 与世界模型提供低成本 3D 感知数据流，降低机器人训练的数据采集门槛。')
    if 'the haves and have nots' in h:
        return ('AI 淘金热的贫与富', 'TechCrunch 深度解读 AI 黄金十年资源分配：大厂凭资本超级周期主导算力与人才，中小组靠开源模型、垂直 Agent 和跟随策略分一杯羹。')
    if 'arxiv will ban authors' in h or ('arxiv' in h and ('ban' in h or 'year' in h)):
        return ('ArXiv 宣布新规：AI 全自动写作论文作者禁投 1 年', '著名预印本平台 ArXiv 新规：若作者让 AI 独立完成全文写作且标注不足，暂停投稿权限 1 年，学术 AI 边界之战进入规则制定阶段。')
    if 'greg brockman' in h and ('product' in h or 'charge' in h):
        return ('OpenAI 联创 Greg Brockman 接管产品战略', 'OpenAI 联创 Greg Brockman 正式负责公司产品战略，从模型路线图到商业化落地全面参与决策，标志 OpenAI 组织架构新阶段。')
    if 'silicon valley' in h and 'vacationland' in h:
        return ('硅谷度假区急需新电力供应商，AI 用电正推高电价', '加州 Monterey 半岛单电来源难撑夏季高峰，AI 数据中心用电叠加推高电价，当地不得不在高价下寻找新供电商，AI 与电网矛盾向外扩散。')
    if 'openai trial wraps up' in h or 'musk founder machine' in h:
        return ('OpenAI 庭审收尾，马斯克创始机器持续运转', 'OpenAI 与马斯克法律博弈方兴未艾，马斯克借 AI 叙事把创始神话一路演到硅谷聚光灯，TechCrunch 从法律与产业维度复盘。')
    if 'cerebras' in h and '60b' in h:
        return ('[AI新闻] Cerebras 惊天 IPO：600 亿美元慢跑后全力冲刺', 'AI 芯片明星 Cerebras 首日收盘 280 美元市值 600 亿美元，与 OpenAI 签署大规模部署协议后 TSMC 产能成 2028 年前持续瓶颈。')
    if 'everything is conductor' in h:
        return ('[AI新闻] 万物皆指挥台——AI 架构新范式蔓延', '本轮围绕指挥台模式的讨论在 AI 工程架构中持续扩散。Cerebras、Runway、Abridge 三家技术路线在指挥台视角下有了共同方法论。')
    if 'ai-native healthcare' in h:
        return ('AI 原生医疗：亿次诊疗单次省 10-20 工时，前置授权立等可取', 'Abridge 2018 年成立，今年预计服务超 8000 万患者覆盖 250 家美国大型医疗体系，正从前置记录扩展到全流程 AI 代理。')
    if 'codex rises' in h:
        return ('[AI新闻] Codex 加速崛起，Claude 计量程序化 API 调用量', 'Codex 在开发者侧攻城，Claude 悄然推出按程序调用次计费，API 用量分层正式进入实测，数据正为 2026 AI 商业化提供标尺。')
    if 'end of finetuning' in h:
        return ('[AI新闻] 微调的终结——长提示词工程成 2026 核心技能', 'OpenAI 弃用精调 API 引发热议，但顶级 AI 开发商增加开源 RL 精调——路径从端到端换成长提示词工程加推理强化。')
    return None

missed = []
for n in top15:
    key = n['title']
    t = get_trans(key, n.get('source',''))
    if t:
        n['title_zh'], n['summary_zh'] = t
    else:
        n['title_zh']   = key
        n['summary_zh'] = f'关于「{key}」的报道。（{n.get("source","")}）'
        missed.append(key)

print('Unmatched:', missed if missed else 'None ✓')
print(f'Total translated: {sum(1 for n in top15 if n.get("title_zh") and n["title_zh"] != n["title"])}/15')

# ── Build HTML ──────────────────────────────────────────────────────────
def trunc(s, mx=105):
    s = s.strip()
    if len(s) <= mx: return s
    for p in '。！？；':
        pos = s[:mx].rfind(p)
        if pos > 20: return s[:pos+1]
    for p in '，、.':
        pos = s[:mx].rfind(p)
        if pos > 20: return s[:pos+1]
    return s[:mx-3] + '…'

def section(name, items, color, sources):
    fi = [n for n in items if n['source'] in sources]
    if not fi: return ''
    fi.sort(key=lambda x: x.get('score',0), reverse=True)
    rows = []
    for i, n in enumerate(fi):
        t = n.get('title_zh') or n['title'] or ''
        s = n.get('summary_zh') or ''
        if s.startswith(t): s = s[len(t):].strip()
        s = s.lstrip(':：— \t')
        s = trunc(s)
        rows.append(
            f'<div style="padding:8px 0;border-bottom:1px solid #f0f0f0;">'
            f'<div style="font-size:15px;font-weight:700;line-height:1.5;margin-bottom:2px;color:#111">'
            f'{i+1}. <a href="{n["url"]}" style="text-decoration:none;color:#1976d2">{t}</a>'
            f'</div><div style="font-size:13px;color:#555;line-height:1.6">{s}</div></div>'
        )
    return (
        f'<div style="margin:16px 0 0">'
        f'<h3 style="font-size:18px;font-weight:800;color:{color};margin:0 0 10px;'
        f'padding-bottom:6px;border-bottom:2px solid {color}">{name}</h3>'
        f'  <div style="padding:0 4px">\n' + '\n'.join(rows) + '\n</div>\n  </div>'
    )

def img_for(i):
    t = (i.get('title_zh','') or i.get('title','')).lower()
    if any(k in t for k in ('robot','agent','智能体','robotics','humanoid','film','filmmaker','video','movie','语音','3d')):
        return 'https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=900&h=383&fit=crop&q=80'
    return 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&h=383&fit=crop&q=80'

blocks = '\n'.join(filter(None, [
    section('TechCrunch AI', top15, '#1a73e8', ['TechCrunch']),
    section('Hacker News',  top15, '#ff6b35', ['HackerNews']),
    section('Substack',     top15, '#9c27b8', ['LatentSpace','TheDecoder','MITTechReview']),
]))

hl       = top15[0]
hl_title = hl.get('title_zh') or hl['title']
hl_score = hl.get('score',0)
imgv     = img_for(hl)

html = (
    '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">'
    f'<title>AI news {DATE}</title>'
    '<style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.55;color:#333;margin:0;padding:0;background:#fff}'
    'a{color:#1976d2;text-decoration:none}img{max-width:100%;border-radius:8px}</style></head><body>'
    f'<div style="text-align:center;padding:28px 16px 20px;border-bottom:1px solid #e65100">'
    f'<div style="font-size:22px;font-weight:800;color:#111;line-height:1.4;margin-bottom:8px">{hl_title}</div>'
    f'<img src="{imgv}" style="width:100%;max-width:580px;border-radius:10px;margin:12px auto 8px;display:block" alt="">'
    f'<div style="font-size:12px;color:#999;margin-top:4px">{DATE} · 共{len(all_n)}条 · HN · TC · LS · TD · MIT</div></div>'
    f'\n{blocks}'
    f'<div style="text-align:center;padding:24px 0 40px;color:#bbb;font-size:12px;border-top:1px solid #eee;margin-top:28px">'
    '<p style="margin:0 0 6px">数据来源：Hacker News · TechCrunch · Latent Space · The Decoder · MIT Technology Review</p>'
    '<p style="margin:0">由 AI News Publisher 自动生成 · 每日 07:00 更新</p></div></body></html>'
)

(DATA / f'news-{DATE}.json').write_text(
    json.dumps({'date':DATE,'news':all_n}, ensure_ascii=False, indent=2), 'utf8')
out = DATA / f'wechat-html-{DATE}.html'
(DATA / f'wechat-html-{DATE}-{int(time.time()*1000)}.html').write_text(html, 'utf8')
out.write_text(html, 'utf8')

print(f'\u2705 {DATE} HTML  {len(html):,} chars')
print(f'   Headline: {hl_title}  (score={hl_score})')
en = [n['title'] for n in top15 if not n.get('title_zh') or n['title_zh']==n['title']]
print(f'   EN left: {en if en else "None \u2713"}')
print(f'   File: {out}')
