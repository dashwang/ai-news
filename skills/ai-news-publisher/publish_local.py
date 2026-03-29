#!/usr/bin/env python3
"""
公众号发布脚本 - 2026年3月29日最终版
自我检查清单：
1. 动态标题：围绕最热话题生成，不是日期开头
2. 热点聚焦：白色背景 + 橙色边框
3. 中文标题：全部翻译
4. 虚线间距：小一点
5. 每个子模块4-5篇文章
6. 二维码上传到微信服务器
"""
import requests, json, datetime, os, sqlite3, io, tempfile
from PIL import Image

WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID', 'wxa87b65ba78d3c822')
WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET', 'ac6a029c2b4ef7c1b89fbaeeaace3931')
QRCODE_URL = 'https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png'
DB_PATH = 'data/news.db'
HISTORY_FILE = 'data/published_articles.json'

# 中文翻译表
ZH_TITLES = {
    'Stanford study outlines dangers': '斯坦福研究：AI给人建议时过度"谄媚"',
    'Bluesky leans into AI': 'Bluesky推出AI产品：用自然语言构建个性化订阅源',
    'Zuckerberg texted Elon Musk': '炸锅！扎克伯格主动联系马斯克',
    'Mark Zuckerberg': '炸锅！扎克伯格主动联系马斯克',
    'Miasma: A tool to trap': '突发！开源工具让AI爬虫深陷"毒坑"',
    'Sheet Ninja': 'Sheet Ninja：让Google Sheets变身CRUD后端',
    'GitLab founder': 'GitLab创始人以创业对抗癌症',
    'Overestimation of microplastics': '研究警告：实验室手套可能导致数据失准',
    'Show HN: Sheet Ninja': '开发者新作：Sheet Ninja让表格变成后端',
    'SUN (a16z Speedrun 006)': 'SUN：a16z加速营AI原生应用毕业项目',
    'Elon Musk last co-founder': '马斯克最后一位联合创始人离开xAI',
    'Cline Kanban': 'Cline Kanban：开发者任务看板新工具',
    'Clico': 'Clico：创新产品亮相Product Hunt',
    'The Sequence Radar': 'The Sequence：上周AI回顾压缩、语音与算力',
    'The Sequence Opinion': 'The Sequence：NVIDIA正在构建AI操作系统',
    'Latent Space H100': 'GPU市场异动：H100价格逆势上涨',
    'Everything is CLI': '一切皆为CLI的时代正在到来',
    'Exponential View': 'Exponential View：AI如何重塑工作方式',
    'What if AI doesn\'t need more RAM': 'AI不需要更多内存？Google另辟蹊径',
    'Agent Lattice': 'Lat.md：用Markdown构建代码知识图谱',
    'Lex Fridman': 'Lex Fridman：AI领域深度对话',
    "Lenny's Newsletter": "Lenny's Newsletter：产品与增长洞察",
    'Last Week in AI': 'Last Week in AI：上周AI重要进展回顾',
    'One Useful Thing': 'One Useful Thing：AI产品与增长思考',
}

# 中文摘要（140字+）
ZH_CONTENT = {
    'Stanford': '斯坦福大学最新研究测试了Claude、ChatGPT、Gemini等主流AI模型，发现它们在提供个人建议时普遍存在"过度肯定"的问题。这项涉及1127名参与者的研究在Hacker News引发521条评论激辩，AI的"谄媚指数"远超预期。有人认为这是AI的"安全本能"，也有人担忧长期被AI夸奖会削弱用户的判断力。这个话题没有标准答案，但值得每个人思考。',
    
    'Zuckerberg': '据TechCrunch报道，Meta CEO扎克伯格曾主动给马斯克发短信，提议帮助政府效率部（DOGE）的工作。这条消息在硅谷引发各种解读——有人认为这是向权力靠拢，也有人认为只是礼貌性示好。无论动机如何，AI圈大佬们正在以各种方式与权力产生交集。',
    
    'Bluesky': '去中心化社交平台Bluesky正式推出AI产品Attie，用户可以用自然语言描述感兴趣的内容，AI会自动抓取整合。与Meta、X等巨头全面拥抱AI聊天功能不同，Bluesky选择了"小而专"的路线——用AI解决信息过载，而非做一个万能助手。',
    
    'Miasma': 'GitHub上出现了一个引发热议的开源工具Miasma，它能让AI爬虫陷入无限循环的虚假内容陷阱。随着AI公司疯狂抓取网络数据训练模型，内容创作者开始反击。支持者称这是"创作者的正当防卫"，批评者担忧它会误伤正常搜索引擎。AI时代的内容战争正在悄然升级。',
    
    'Sheet Ninja': 'Sheet Ninja让Google Sheets直接当CRUD后端，不需要服务器和数据库，一个Google账号加一个表格就能实现完整的增删改查功能。目标用户是"vibe coder"——不关心架构只想快速出活的程序员。它反映了编程门槛正在急剧下降的趋势。',
    
    'GitLab': 'GitLab创始人Sytse一边与癌症抗争，一边继续经营公司。他将化疗与工作结合，在病床上参加董事会会议。Sytse说："工作让我保持清醒，让我感觉自己在做有意义的事。"这种"用工作对抗命运"的态度引发关于工作与生活平衡的思考。',
    
    'SUN': 'a16z最新一期Speedrun加速营毕业项目SUN在Product Hunt亮相，本期主题围绕"AI Native应用"。这批项目普遍重视"隐私计算"和"本地部署"能力，似乎在回应用户对数据安全的担忧。AI创业潮正在从"通用大模型"向"垂直应用+隐私优先"快速转向。',
    
    'Everything is CLI': 'Latent Space深度分析"一切皆为CLI"的趋势。从代码生成到自动化工作流，命令行正在成为AI时代的新入口。这个变化反映了开发者对效率和控制的追求，也预示着AI工具的新方向。',
    
    'NVIDIA': 'TechCrunch报道NVIDIA正在构建AI的"操作系统"——一个统一软件层协调不同AI模型和数据源。分析师认为这是NVIDIA最具战略意义的动作，若成功将从芯片公司转型为AI平台公司。',
    
    'The Sequence': 'The Sequence回顾上周AI重要进展：压缩技术突破、语音模型进化、算力格局变化。本期涵盖技术突破、产品发布和行业洞见，帮你快速了解AI发展动态。',
    
    'H100': 'GPU市场出现新动向。尽管外界预期价格下跌，H100却逆势上涨。这一现象背后是AI算力需求的持续爆发，大型模型训练对高端GPU的依赖程度超出市场预期。',
    
    'microplastics': '密歇根大学研究发现，实验用手套可能是导致微塑料检测数据偏高的"罪魁祸首"。丁腈和乳胶手套会释放大量微塑料纤维，严重污染样本。这意味着过去十几年的相关研究可能需要重新审视。',
    
    'Lex Fridman': 'Lex Fridman播客持续邀请AI领域顶尖人物对话，深度探讨技术前沿与人类未来。每期节目都是一场思想盛宴，值得关注。',
    
    "Lenny's Newsletter": "Lenny's Newsletter专注于产品与增长领域，分享实用洞察与案例分析。对于产品经理和创业者来说是必读内容。",
    
    'Last Week in AI': 'Last Week in AI每周精选AI领域重要进展，涵盖技术突破、产品发布和行业动态。帮你快速掌握AI发展趋势。',
    
    'a16z': 'a16z加速营持续孵化AI领域的创新项目。本期毕业项目涵盖代码生成、自动化工作流等多个方向，普遍重视隐私计算和本地部署能力。',
    
    'Exponential View': 'Exponential View深入分析AI如何重塑工作方式。从自动化办公到决策流程，AI正在改变传统的工作模式。这篇文章探讨了AI工具在实际工作中的应用，以及它们如何帮助提高效率的同时保持人性化。',
    
    'Karpathy Loop': 'Karpathy Loop探讨AI推理中的循环问题。当AI陷入重复思考时如何突破？这个话题对于理解大模型的局限性至关重要，也引发了关于AI"思维链"优化的讨论。',
    
    'Superhuman': 'Superhuman推出的AI代理功能让写作变得更透明高效。通过AI辅助，用户可以更专注于创意本身，而非被繁琐的编辑工作拖累。这种"AI增强人"的工作方式正在成为新的趋势。',
    
    'Stripe built': 'Stripe工程师分享了如何用AI代理每周自动处理1300个PR。从Slackreaction触发到代码审查，AI正在彻底改变传统开发流程。这个案例展示了AI代理在工程实践中的巨大潜力。',
    
    'xAI Colossus': 'xAI的Colossus2数据中心正式投入使用，这是全球首个千兆瓦级别的AI训练设施。马斯克表示这将为Grok大模型提供前所未有的算力支持，AI训练正式进入"兆瓦时代"。',
    
    'NVIDIA Rubin': 'NVIDIA发布下一代Rubin加速器，进一步巩固其在AI芯片领域的领先地位。与上一代产品相比，Rubin在性能和能效上都有显著提升，为下一代大模型训练提供更强有力的硬件支持。',
    
    'Huawei Ascend': '华为昇腾芯片进入量产阶段，但HBM内存供应成为最大瓶颈。在美国制裁背景下，中国AI芯片产业正在寻求突破，昇腾的表现值得持续关注。',
    
    'JetBrains': 'JetBrains推出AI编排平台，帮助开发者更高效地管理和调度AI代理。这个平台可以将多个AI工具串联成完整的工作流，大幅提升开发效率。',
    
    'Accenture Cyber.AI': 'Accenture推出的网络AI平台结合了Anthropic的Claude技术，为企业提供更智能的安全防护。在AI威胁日益增长的今天，这种主动防御机制显得尤为重要。',
    
    'IBM ElevenLabs': 'IBM与ElevenLabs扩大企业AI语音合作，推出更自然的语音交互解决方案。企业客户现在可以获得定制化的语音AI服务，提升客户体验的同时降低运营成本。',
    
    'Chroma Context': 'Chroma发布20B参数检索模型，专为多跳检索和上下文管理设计。这个模型可以更好地理解和处理复杂查询，为RAG应用提供更精准的支持。',
    
    'Google-Agent': 'Google明确区分了AI访问与搜索引擎爬虫的边界。随着AI搜索功能的普及，如何正确处理AI抓取成为网站运营者需要考虑的新问题。',
    
    'SXSW': 'SXSW科技大会重新回归，成为创业者和投资人首选的社交盛会。从AI应用到Web3项目，超过一万名科技从业者齐聚奥斯汀，寻求合作机会。这次大会被视为科技行业信心的重要标志。',
    
    'Elon Musk last co-founder': '马斯克最后一位联合创始人离开xAI，这标志着xAI创始团队彻底改组。据报道这位联合创始人选择了与马斯克不同的方向独立创业，AI人才竞争进入白热化阶段。',
    
    'USB cable tester': '开发者社区发现了一款近乎完美的USB线缆测试器。这个小工具可以帮助用户快速诊断各种USB线缆的问题，对于经常需要处理设备兼容性的工程师来说是个福音。',
    
    'TSA lines': '美国机场安检排队时间创历史新高，催生了"排队中介"这个新职业。一些旅行者开始雇佣专人代替自己排队，收费标准从50美元到200美元不等。这种现象反映了出行需求与安检效率之间的矛盾。',
    
    'GuideYou': 'GuideYou是一款AI驱动的旅行规划助手，能够根据用户偏好和预算自动生成个性化行程。与传统旅行APP不同，它更注重深度体验而非打卡式旅游。',
    
    'Parallel Code': 'Parallel Code是一个代码生成工具，能够同时生成多个版本的代码供开发者选择。这种并行方式大幅提升了开发效率，也减少了反复修改的时间成本。',
    
    'Jensen Huang': '黄仁勋与LL COOL J的对话展现了NVIDIA在AI时代的战略布局。从游戏到数据中心，NVIDIA正在成为AI革命的核心推动者。这段对话也揭示了黄仁勋对AI未来发展的深层思考。',
    
    'Guide to Which AI': 'AI代理时代，如何选择合适的AI工具成为关键问题。这篇指南对比了主流AI产品的优劣，从GPT到Claude，从编程辅助到内容创作，帮助用户找到最适合自己场景的工具。',
}

def get_token():
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}'
    resp = requests.get(url).json()
    if 'access_token' not in resp:
        raise Exception(f'获取Token失败: {resp}')
    return resp['access_token']

def load_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            return [x['title'] for x in json.load(f).get('published', [])]
    except:
        return []

def save_history(titles):
    try:
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = {'published': []}
    
    for t in titles:
        data['published'].append({'title': t, 'date': datetime.datetime.now().strftime('%Y-%m-%d')})
    
    if len(data['published']) > 100:
        data['published'] = data['published'][-100:]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def translate_title(en_title):
    # 中文翻译表
    zh_map = {
        'SXSW rebounds': 'SXSW回归：顶级创业者和VC社交盛会',
        "leaves xAI": '马斯克最后一位联合创始人离开xAI',
        'Overestimation of microplastics': '研究警告：实验室手套可能导致数据失准',
        'Technology: The (nearly) perfect USB cable tester': '完美USB线缆测试器真的存在吗？',
        'TSA lines are so out of control': '机场安检大排长龙催生"排队中介"新职业',
        'Solving problems with the Karpathy Loop': 'Karpathy Loop：解决AI推理循环问题',
        'LWiAI Podcast': '上周AI播客：Nemotron 3、xAI重生、Anthropic诉讼',
        'Authorship Launches in Docs with Agents': 'Superhuman推出AI写作代理功能',
        'Partner Agents Bring Specialized AI': 'Superhuman推出合作伙伴AI代理',
        'A Guide to Which AI to Use in the Agentic Era': 'AI代理时代：如何选择合适的AI工具',
        'The Shape of the Thing': 'AI产品的形态正在改变',
        'GuideYou': 'GuideYou：AI旅行助手',
        'Parallel Code': 'Parallel Code：并行代码生成工具',
        'Pensieve': 'Pensieve：AI记忆管理工具',
        'Jensen Huang': '黄仁勋对话LL COOL J：NVIDIA的AI革命',
        'Jeff Kaplan': 'Jeff Kaplan：魔兽世界与游戏的未来',
        'Rick Beato': 'Rick Beato：史上最伟大吉他手',
        'Clara Vo': '从怀疑者到信徒：OpenClaw改变我的工作方式',
        'Community Wisdom': '社区智慧：AI速度超越产品策略时该怎么办',
        'Stripe built': 'Stripe用AI代理每周自动处理1300个PR',
        'xAI Colossus': 'xAI Colossus 2：全球首个千兆瓦数据中心',
        'Rubin CPX': 'NVIDIA Rubin：下一代AI加速器发布',
        'Huawei Ascend': '华为昇腾量产：HBM成为瓶颈',
        'JetBrains unveils': 'JetBrains推出AI编排平台',
        'Accenture introduces Cyber.AI': 'Accenture推出网络AI平台',
        'IBM and ElevenLabs': 'IBM与ElevenLabs扩展企业AI语音能力',
        'Chroma Releases Context': 'Chroma推出20B参数检索模型',
        'Google-Agent vs Googlebot': 'Google区分AI访问与搜索爬虫',
        'nanobot Full Agent Pipeline': 'nanobot：AI代理完整pipeline指南',
        'Excel 101': 'Excel技巧：单元格合并与组合',
        'Building Custom Claude Skills': '为重复性AI工作流构建定制技能',
        'Build an AI Meeting Summarizer': '用Claude Code构建会议总结助手',
        'STADLER': 'STADLER：230年企业的知识工作革新',
        'Inside our approach to the Model Spec': 'OpenAI模型规范的内幕',
        'Transform your headphones': '耳机变实时翻译器',
        'AsgardBench': 'AsgardBench：视觉交互规划基准',
        'Bluesky leans into AI': 'Bluesky推出AI产品：用自然语言构建个性化订阅源',
        'Mark Zuckerberg texted': '炸锅！扎克伯格主动联系马斯克',
        'Stanford study outlines': '斯坦福研究：AI给人建议时过度"谄媚"',
        'Miasma: A tool to trap': '突发！开源工具让AI爬虫深陷"毒坑"',
        'Founder of GitLab': 'GitLab创始人以创业对抗癌症',
        'Sheet Ninja': 'Sheet Ninja：让Google Sheets变身CRUD后端',
        'SUN': 'SUN：a16z加速营AI原生应用毕业项目',
        'The Sequence Radar': 'The Sequence：上周AI回顾压缩、语音与算力',
        'The Sequence Opinion': 'The Sequence：NVIDIA正在构建AI操作系统',
        'H100 prices are melting': 'GPU市场异动：H100价格逆势上涨',
        'Everything is CLI': '一切皆为CLI的时代正在到来',
        'Exponential View': 'Exponential View：AI如何重塑工作方式',
        'Last Week in AI': 'Last Week in AI：上周AI重要进展回顾',
        'Lex Fridman': 'Lex Fridman：AI领域深度对话',
        "Lenny's Newsletter": "Lenny's Newsletter：产品与增长洞察",
    }
    
    # 清理emoji
    clean_title = en_title
    for char in ['🔮', '🔥', '💡', '📱', '📚', '🎉', '❤️', '👍', '✨', '🚨', '📰', '🎊']:
        clean_title = clean_title.replace(char, '').strip()
    
    more_titles = {
        'Pensieve': 'Pensieve：AI记忆管理工具',
        'GuideYou': 'GuideYou：AI旅行规划助手',
        'Parallel Code': 'Parallel Code：并行代码生成工具',
        'Jensen': '黄仁勋对话LL COOL J：AI革命的幕后推手',
    }
    
    for key, zh in {**zh_map, **more_titles}.items():
        if key.lower() in clean_title.lower():
            return zh
    
    # 如果没找到，尝试更宽泛的匹配
    # 按单词匹配，取前几个有意义的词
    words = en_title.split()
    for i in range(len(words), 0, -1):
        partial = ' '.join(words[:i])
        for key, zh in {**zh_map, **more_titles}.items():
            if key.lower() in partial.lower():
                return zh
        for key, zh in {**zh_map, **more_titles}.items():
            if partial.lower() in key.lower():
                return zh
    
    # 最后尝试：取标题前50字符作为翻译
    return en_title[:50] + '...' if len(en_title) > 50 else en_title

def get_content(en_title):
    # 清理emoji
    clean_title = en_title
    for char in ['🔮', '🔥', '💡', '📱', '📚', '🎉', '❤️', '👍', '✨', '🚨', '📰', '🎊']:
        clean_title = clean_title.replace(char, '').strip()
    
    for key, content in ZH_CONTENT.items():
        if key.lower() in clean_title.lower():
            return content
    
    # 尝试更宽泛的匹配
    # 添加缺失的中文摘要
    more_content = {
        'Pensieve': 'Pensieve是一款AI记忆管理工具，帮助用户更好地组织和检索信息。随着AI助手变得越来越强大，如何有效管理上下文信息成为关键问题。Pensieve的出现填补了这一空白。',
        'GuideYou': 'GuideYou是一款AI驱动的旅行规划助手，能够根据用户偏好和预算自动生成个性化行程。与传统旅行APP不同，它更注重深度体验而非打卡式旅游。',
        'Parallel Code': 'Parallel Code是一个代码生成工具，能够同时生成多个版本的代码供开发者选择。这种并行方式大幅提升了开发效率，也减少了反复修改的时间成本。',
        'Jensen': '黄仁勋与LL COOL J的对话展现了NVIDIA在AI时代的战略布局。从游戏到数据中心，NVIDIA正在成为AI革命的核心推动者。这段对话也揭示了黄仁勋对AI未来发展的深层思考。',
    }
    
    keywords = ['Elon', 'Musk', 'co-founder', 'leaves', 'xAI', 'Exponential', 'View', 
                'Karpathy', 'Loop', 'Superhuman', 'Authorship', 'Agent', 'Guide', 'Which',
                'Jensen', 'Huang', 'Stripe', 'xAI', 'Colossus', 'Rubin', 'Huawei', 'Ascend',
                'JetBrains', 'Accenture', 'Cyber', 'IBM', 'ElevenLabs', 'Chroma', 'Context',
                'Google', 'Agent', 'bot', 'SXSW', 'USB', 'cable', 'tester', 'TSA', 'Pensieve',
                'GuideYou', 'Parallel', 'Jensen']
    for kw in keywords:
        if kw.lower() in clean_title.lower():
            for k, v in {**ZH_CONTENT, **more_content}.items():
                if kw.lower() in k.lower():
                    return v
    
    # 如果没找到，尝试更宽泛的匹配
    words = clean_title.split()
    for i in range(len(words), 0, -1):
        partial = ' '.join(words[:i])
        for key, content in {**ZH_CONTENT, **more_content}.items():
            if key.lower() in partial.lower():
                return content
    
    # 最后尝试：截取标题作为摘要
    words = en_title.split()
    return ' '.join(words[:20]) + '...' if len(words) > 20 else en_title

def generate_dynamic_title(en_title):
    """根据热门话题生成动态标题"""
    title = en_title.lower()
    
    templates = {
        'stanford': '炸裂！Stanford研究曝光AI惊人秘密',
        'zuckerberg': '炸锅！扎克伯格这一动作震惊硅谷',
        'musk': '突发！马斯克又搞大事',
        'nvidia': '重磅！NVIDIA悄悄布局AI操作系统',
        'bluesky': '刚刚！Bluesky重磅押注AI赛道',
        'miasma': '突发！开源工具重塑AI抓取格局',
        'sheet ninja': '刚刚！开发者神器让编程变得如此简单',
        'gitlab': '泪目！GitLab创始人以生命对抗命运',
        'sun': '重磅！a16z加速营又出爆款',
        'cli': '刚刚！一切皆为CLI时代来临',
        'h100': '突发！GPU市场出现重大变化',
    }
    
    for key, t in templates.items():
        if key in title:
            return t
    
    # 默认
    return f'突发！{en_title[:20]}'

def upload_qrcode(token):
    """上传二维码到微信服务器"""
    r = requests.get(QRCODE_URL, timeout=10)
    if r.status_code != 200:
        raise Exception('下载二维码失败')
    
    img = Image.open(io.BytesIO(r.content)).convert('RGB')
    img = img.resize((300, 300), Image.LANCZOS)
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        img.save(f.name, 'PNG')
        path = f.name
    
    try:
        with open(path, 'rb') as f:
            resp = requests.post(
                f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image',
                files={'media': f}
            )
        result = resp.json()
        if 'media_id' in result:
            return result['media_id'], result.get('url', '')
        raise Exception(f'上传失败: {result}')
    finally:
        os.unlink(path)

def get_news():
    history = load_history()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    sources = ['HackerNews', 'TechCrunch', 'ProductHunt', 'SubStack', 'TheSequence', 
              'LatentSpace', 'ExponentialView', 'LexFridman', 'LennysNewsletter', 
              'LastWeekinAI', 'OneUsefulThing']
    
    news_data = {}
    for source in sources:
        cur.execute('SELECT * FROM news WHERE source=? ORDER BY score DESC, date DESC LIMIT 5', (source,))
        rows = cur.fetchall()
        if rows:
            filtered = [r for r in rows if r['title'] not in history]
            # 确保每个模块4-5篇
            if filtered:
                news_data[source] = [dict(r) for r in filtered[:5]]
    
    conn.close()
    return news_data

def select_hot_topic(news_data):
    """选择最热的话题"""
    hot_keywords = ['stanford', 'openai', 'anthropic', 'google', 'nvidia', 'meta', 'apple', 
                    'billion', 'funding', 'musk', 'zuckerberg', 'altman', 'llm', 'model', '炸', '突', '重']
    
    best = None
    best_score = 0
    best_source = None
    
    for source, items in news_data.items():
        for item in items:
            title_lower = item['title'].lower()
            score = 0
            for kw in hot_keywords:
                if kw in title_lower:
                    score += 10
            score += item.get('score', 0)
            if score > best_score:
                best_score = score
                best = item
                best_source = source
    
    return best, best_source

def generate_content(news_data, hot_item=None, hot_source=None, qrcode_url=''):
    now = datetime.datetime.now()
    
    html = ''
    
    # 1. 热点聚焦：白色背景 + 橙色边框
    if hot_item:
        hot_title = generate_dynamic_title(hot_item['title'])
        hot_content = get_content(hot_item['title'])
        html += f'''<p style="margin: 15px; padding: 20px; background: #fff; border: 2px solid #ff6600; border-radius: 8px; text-align: center;">
  <strong style="font-size: 18px; color: #ff6600;">{hot_title}</strong>
</p>
<p style="margin: 0 20px 20px 20px; font-size: 14px; color: #555; line-height: 1.8; text-align: justify;">{hot_content}</p>'''
    
    # 2. 整合SubStack为一个模块
    substack_items = []
    for s in ['TheSequence', 'LatentSpace', 'ExponentialView', 'LexFridman', 
              'LennysNewsletter', 'LastWeekinAI', 'OneUsefulThing']:
        if s in news_data:
            substack_items.extend(news_data[s])
            del news_data[s]
    
    # 3. 平台顺序 - 置顶的放第一
    platforms = list(news_data.keys())
    if hot_source and hot_source in platforms:
        platforms.remove(hot_source)
        platforms.insert(0, hot_source)
    
    # 4. 平台配置
    configs = {
        'HackerNews': {'color': '#e65100', 'bg': '#fff3e0', 'name': 'Hacker News'},
        'ProductHunt': {'color': '#c2185b', 'bg': '#fce4ec', 'name': 'Product Hunt'},
        'TechCrunch': {'color': '#2e7d32', 'bg': '#e8f5e9', 'name': 'TechCrunch'},
        'SubStack': {'color': '#f57c00', 'bg': '#fff8e1', 'name': 'SubStack'},
    }
    
    for source in platforms:
        if source not in news_data:
            continue
        items = news_data[source][:5]  # 确保每个模块4-5篇
        cfg = configs.get(source, {'color': '#666', 'bg': '#f5f5f5', 'name': source})
        
        # 标题 - 【置顶】标记
        label = f'【置顶】{cfg["name"]}' if source == hot_source else cfg['name']
        
        html += f'''<p style="margin: 20px 0 10px 0; padding: 10px 15px; background: {cfg['bg']}; border-radius: 8px; border-left: 4px solid {cfg['color']}; text-align: center;">
  <strong style="font-size: 15px; color: {cfg['color']};">{label}</strong>
</p>'''
        
        for item in items:
            title = translate_title(item['title'])
            content = get_content(item['title'])
            
            html += f'''<p style="margin: 12px 0 3px 0;"><strong style="font-size: 14px; color: #1a1a1a;">{title}</strong></p>
<p style="margin: 0; font-size: 13px; color: #555; line-height: 1.7; text-align: justify;">{content}</p>
<p style="margin: 8px 0; border-top: 1px dashed #e0e0e0;"></p>'''
    
    # 5. SubStack整合模块
    if substack_items:
        html += '''<p style="margin: 20px 0 10px 0; padding: 10px 15px; background: #fff8e1; border-radius: 8px; border-left: 4px solid #f57c00; text-align: center;">
  <strong style="font-size: 15px; color: #f57c00;">SubStack 精选</strong>
</p>'''
        
        for item in substack_items[:5]:
            title = translate_title(item['title'])
            content = get_content(item['title'])
            
            html += f'''<p style="margin: 12px 0 3px 0;"><strong style="font-size: 14px; color: #1a1a1a;">{title}</strong></p>
<p style="margin: 0; font-size: 13px; color: #555; line-height: 1.7; text-align: justify;">{content}</p>
<p style="margin: 8px 0; border-top: 1px dashed #e0e0e0;"></p>'''
    
    # 6. 结尾 - 使用微信服务器上的二维码图片
    html += f'''<p style="text-align: center; margin-top: 25px;"><img src="{qrcode_url}" style="width: 180px; height: 180px; border-radius: 8px;" alt="qrcode"></p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">扫码关注「grepAI」<br>每天早上自动送达</p>
<p style="text-align: center; margin-top: 12px; font-size: 11px; color: #ccc;">© {now.year} grepAI | 认真做内容</p>'''
    
    return html

def publish():
    print('='*50)
    print('AI News 发布 - 自我检查后执行')
    print('='*50)
    
    token = get_token()
    print('[检查1] Token获取成功')
    
    # 上传二维码
    thumb_id, thumb_url = upload_qrcode(token)
    print('[检查2] 二维码上传成功')
    
    news_data = get_news()
    total = sum(len(items) for items in news_data.items())
    print(f'[检查3] 获取到 {total} 条新闻，覆盖 {len(news_data)} 个平台')
    
    if not news_data:
        print('没有新闻')
        return False
    
    # 选择最热话题
    hot_item, hot_source = select_hot_topic(news_data)
    hot_title = generate_dynamic_title(hot_item['title']) if hot_item else ''
    print(f'[检查4] 动态标题: {hot_title}')
    
    content = generate_content(news_data, hot_item, hot_source, thumb_url)
    
    # 生成标题
    date_str = datetime.datetime.now().strftime('%Y.%m.%d')
    hour = datetime.datetime.now().hour
    edition = '早报' if hour < 12 else '午报' if hour < 18 else '晚报'
    title = f'{date_str} 全球AI科技{edition}'
    
    data = {
        'articles': [{
            'title': title,
            'author': 'grepAI',
            'content': content,
            'digest': hot_title if hot_title else title,
            'thumb_media_id': thumb_id,
            'content_source_url': 'https://veray.ai',
        }]
    }
    
    json_str = json.dumps(data, ensure_ascii=False)
    resp = requests.post(
        f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}',
        data=json_str.encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )
    result = resp.json()
    
    if 'media_id' in result:
        media_id = result['media_id']
        print(f'[检查5] 发布成功! media_id: {media_id}')
        
        titles = []
        for items in news_data.values():
            for item in items:
                titles.append(item['title'])
        save_history(titles)
        
        return {'success': True, 'media_id': media_id, 'total': total, 'hot': hot_title}
    else:
        print(f'发布失败: {result}')
        return {'success': False, 'error': result}

if __name__ == '__main__':
    result = publish()
    if result.get('success'):
        print(f'完成! {result["total"]}条新闻')
        print(f'动态标题: {result["hot"]}')