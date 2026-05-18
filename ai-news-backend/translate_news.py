#!/usr/bin/env python3
"""
Translate and format AI news for WeChat publication
"""

import json

# Load news data
with open('/root/.openclaw/workspace/ai_news.json', 'r') as f:
    data = json.load(f)

news = data['news']

# Translate and format
html = '''<p style="text-align: center; font-size: 22px; font-weight: bold;">🔥 2026.02.27 科技早报</p>
<p style="text-align: center; color: #888; font-size: 13px;">今日精选 · 20条新闻</p>

<p><strong>🤖 Hacker News 热门 (5条)</strong></p>
<p>1. <strong>Dario Amodei回应五角大楼：不会向军方开放AI系统</strong> - Anthropic CEO明确表示"问心无愧"地拒绝军方要求</p>
<p>2. <strong>黑暗早餐的追踪</strong> - 探索早餐麦片背后的神秘故事</p>
<p>3. <strong>2003论文：组织腐败的常态化</strong> - 学术研究揭示腐败如何成为常态</p>
<p>4. <strong>Julia性能优化技巧</strong> - 官方性能优化指南</p>
<p>5. <strong>80386保护模式</strong> - 深入理解x86架构</p>

<p><strong>💡 Lenny's Newsletter (5条)</strong></p>
<p>1. <strong>Cisco总裁：AI对人类生存至关重要</strong> - Jeetu Patel谈AI革命与为何大公司应该全力投入</p>
<p>2. <strong>5个OpenClaw agents管理我的家、理财和代码</strong> - 四娃妈妈分享如何用AI管理生活</p>
<p>3. <strong>如何用AI准备下一次面试</strong> - 30+科技专家的求职AI技巧</p>
<p>4. <strong>本周AI播客：Notion设计团队如何用Claude Code</strong> - AI辅助设计实战</p>
<p>5. <strong>OpenClaw：GitHub史上增长最快的开源项目</strong> - Peter Steinberger谈OpenClaw的诞生</p>

<p><strong>🎙️ Lex Fridman 播客 (5条)</strong></p>
<p>1. <strong>#491 OpenClaw：引爆互联网的病毒式AI Agent</strong> - Peter Steinberger对话Lex</p>
<p>2. <strong>2026年AI现状：LLM、编码、扩展法则、中国、Agent、GPU、AGI</strong> - Nathan Lambert与Sebastian Raschka深度对谈</p>
<p>3. <strong>GSP教Lex街头格斗</strong> - 格斗冠军的实战技巧</p>
<p>4. <strong>《1984》乔治·奥威尔</strong> - Lex读书分享</p>
<p>5. <strong>OpenClaw创始人访谈完整 transcript</strong> - 深度了解OpenClaw背后的故事</p>

<p><strong>📱 TechCrunch 科技 (5条)</strong></p>
<p>1. <strong>Plaid估值达80亿美元</strong> - 员工股份出售，估值较4月增长31%</p>
<p>2. <strong>Netflix退出竞购Warner Bros</strong> - David Ellison的Paramount将收购Warner Bros Discovery</p>
<p>3. <strong>Jack Dorsey大幅裁员：Block员工减半</strong> - 他说下一个就是你公司</p>
<p>4. <strong>Anthropic CEO坚决抵抗五角大楼</strong> - 拒绝向军方开放AI系统</p>
<p>5. <strong>PayPal可能不卖了</strong> - 报道称Stripe曾考虑收购但目前无实质谈判</p>

<p style="text-align: center; margin-top: 20px;">📱 关注我们，获取每日科技前沿！</p>
'''

print(html)
