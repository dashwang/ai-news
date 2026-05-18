#!/usr/bin/env python3
"""
公众号发布脚本 - 2026年3月29日最新版
格式要求：
1. 热点聚焦模块 - 白色背景 + 橙色边框
2. InfoQ风格子标题：简洁朴素，无彩色边框
3. 动态标题
4. 所有内容翻译成中文
"""
import requests, json, datetime, os, sqlite3, io, tempfile, random
from PIL import Image
import requests, json, datetime, os, sqlite3, io, tempfile
from PIL import Image

WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID', 'wxa87b65ba78d3c822')
WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET', 'ac6a029c2b4ef7c1b89fbaeeaace3931')
QRCODE_URL = 'https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png'
DB_PATH = 'data/news.db'
HISTORY_FILE = 'data/published_articles.json'

# 配图映射表
IMAGE_MAP = {
    '扎克伯格': 'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400&h=300&fit=crop',
    '马斯克': 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=400&h=300&fit=crop',
    'OpenAI': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=300&fit=crop',
    'Anthropic': 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=400&h=300&fit=crop',
    'NVIDIA': 'https://images.unsplash.com/photo-1591238372338-22d30c883a86?w=400&h=300&fit=crop',
    'GPU': 'https://images.unsplash.com/photo-1591238372338-22d30c883a86?w=400&h=300&fit=crop',
    'H100': 'https://images.unsplash.com/photo-1591238372338-22d30c883a86?w=400&h=300&fit=crop',
    'CLI': 'https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=400&h=300&fit=crop',
    'Terminal': 'https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=400&h=300&fit=crop',
    'Code': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=300&fit=crop',
    'GitLab': 'https://images.unsplash.com/photo-1618401471357-b6af6d0f9f77?w=400&h=300&fit=crop',
    'Bluesky': 'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400&h=300&fit=crop',
    'Product': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop',
    'default': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=300&fit=crop',
}

def get_topic_image(title):
    for key, url in IMAGE_MAP.items():
        if key.lower() in title.lower():
            return url
    return IMAGE_MAP['default']

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
    """翻译标题为中文，清理emoji"""
    # 清理emoji
    clean_title = en_title
    for char in ['🔮', '🔥', '💡', '📱', '📚', '🎉', '❤️', '👍', '✨', '🚨', '📰', '🎊', '🧠']:
        clean_title = clean_title.replace(char, '').strip()
    
    zh_map = {
        # 新增翻译
        'The Sequence Radar': 'The Sequence上周AI回顾压缩语音与算力',
        'The Sequence Opinion': 'The Sequence NVIDIA正在构建AI操作系统',
        'The Sequence': 'The Sequence AI领域技术分析',
        'NVIDIA Is Quietly Building': 'NVIDIA正在悄悄构建AI操作系统',
        'H100 prices are melting': 'H100价格逆势上涨GPU市场异动',
        'Everything is CLI': '一切皆为CLI的时代正在到来',
        'Exponential View': 'Exponential View AI如何重塑工作方式',
        'Last Week in AI': 'Last Week in AI上周重要进展回顾',
        'Lex Fridman': 'Lex Fridman AI领域深度对话',
        "Lenny's Newsletter": "Lenny's Newsletter产品与增长洞察",
        'Pixel 10a': 'Pixel 10a取消摄像头凸起设计',
        'YouTube CEO': 'YouTube CEO称最优秀创作者不会离开平台',
        'Project Hail Mary': 'Project Hail Mary成为票房冠军',
        'Sora shutdown': 'Sora关闭为AI视频行业敲响警钟',
        'TechCrunch Mobility': 'TechCrunch Mobility机器人axi呼叫911',
        'Coding Agents': '编程代理可能让自由软件重新崛起',
        'ChatGPT Won\'t Let': 'ChatGPT阻止输入直到读取React状态',
        'Cognitive Dark Forest': '认知黑暗森林',
        'Voyager 1': 'Voyager 1飞船仅靠69KB内存和磁带机运行',
        'Midnight train': '午夜列车从GA出发',
        'CodingPrep': 'CodingPrep编程面试准备工具',
        'Peopling': 'Peopling社交网络分析工具',
        
        # 原有翻译
        'SXSW rebounds': 'SXSW回归顶级创业者和VC社交盛会',
        'Elon Musk last co-founder': '马斯克最后一位联合创始人离开xAI',
        'Overestimation of microplastics': '研究警告实验室手套可能导致数据失准',
        'USB cable tester': '完美USB线缆测试器真的存在吗',
        'TSA lines': '机场安检大排长龙催生排队中介新职业',
        'Karpathy Loop': 'Karpathy Loop解决AI推理循环问题',
        'LWiAI Podcast': '上周AI播客Nemotron 3、xAI重生、Anthropic诉讼',
        'Authorship Launches': 'Superhuman推出AI写作代理功能',
        'Partner Agents': 'Superhuman推出合作伙伴AI代理',
        'Guide to Which AI': 'AI代理时代如何选择合适的AI工具',
        'Shape of the Thing': 'AI产品的形态正在改变',
        'GuideYou': 'GuideYou AI旅行规划助手',
        'Parallel Code': 'Parallel Code并行代码生成工具',
        'Pensieve': 'Pensieve AI记忆管理工具',
        'Jensen Huang': '黄仁勋对话LL COOL J AI革命的幕后推手',
        'Jeff Kaplan': 'Jeff Kaplan论魔兽世界与游戏的未来',
        'Rick Beato': 'Rick Beato探讨史上最伟大吉他手',
        'Clara Vo': '从怀疑者到信徒OpenClaw改变我的工作方式',
        'Community Wisdom': '社区智慧当AI速度超越产品策略',
        'Stripe built': 'Stripe用AI代理每周自动处理1300个PR',
        'xAI Colossus': 'xAI Colossus 2全球首个千兆瓦数据中心',
        'Rubin CPX': 'NVIDIA Rubin下一代AI加速器发布',
        'Huawei Ascend': '华为昇腾量产HBM成为瓶颈',
        'JetBrains unveils': 'JetBrains推出AI编排平台',
        'Cyber.AI': 'Accenture推出网络AI平台',
        'ElevenLabs': 'IBM与ElevenLabs扩展企业AI语音能力',
        'Chroma Releases': 'Chroma推出20B参数检索模型',
        'Google-Agent': 'Google区分AI访问与搜索爬虫边界',
        'nanobot': 'nanobot AI代理完整pipeline指南',
        'Excel 101': 'Excel技巧单元格合并与组合',
        'Claude Skills': '为重复性AI工作流构建定制技能',
        'Meeting Summarizer': '用Claude Code构建会议总结助手',
        'STADLER': 'STADLER 230年企业的知识工作革新',
        'Model Spec': 'OpenAI模型规范的内幕',
        'headphones': '耳机变实时翻译器',
        'AsgardBench': 'AsgardBench视觉交互规划基准',
        'Bluesky leans': 'Bluesky推出AI产品用自然语言构建个性化订阅源',
        'Mark Zuckerberg texted': '炸锅扎克伯格主动联系马斯克',
        'Zuckerberg': '炸锅扎克伯格主动联系马斯克',
        'Stanford study': '斯坦福研究AI给人建议时过度谄媚',
        'Miasma': '突发开源工具让AI爬虫深陷毒坑',
        'Founder of GitLab': 'GitLab创始人以创业对抗癌症',
        'Sheet Ninja': 'Sheet Ninja让Google Sheets变身CRUD后端',
        'SUN': 'SUN a16z加速营AI原生应用毕业项目',
    }
    
    for key, zh in zh_map.items():
        if key.lower() in clean_title.lower():
            return zh
    
    # 默认翻译
    return clean_title[:35] + '...' if len(clean_title) > 35 else clean_title

def get_content(en_title):
    """翻译内容为中文，清理emoji"""
    clean_title = en_title
    for char in ['🔮', '🔥', '💡', '📱', '📚', '🎉', '❤️', '👍', '✨', '🚨', '📰', '🎊', '🧠']:
        clean_title = clean_title.replace(char, '').strip()
    
    zh_map = {
        # 热门新闻
        'Zuckerberg': '据TechCrunch报道，Meta CEO扎克伯格曾主动给马斯克发短信，提议帮助政府效率部DOGE的工作。这条消息在硅谷引发各种解读，有人认为这是向权力靠拢，也有人认为只是礼貌性示好。无论动机如何，AI圈大佬们正在以各种方式与权力产生交集，值得持续关注。',
        
        'The Sequence': 'The Sequence回顾上周AI重要进展：压缩技术突破、语音模型进化、算力格局变化。本期涵盖技术突破、产品发布和行业洞见，帮你快速了解AI发展动态。',
        
        'NVIDIA Is Quietly Building': 'TechCrunch报道NVIDIA正在构建AI的操作系统，一个统一软件层协调不同AI模型和数据源。分析师认为这是NVIDIA最具战略意义的动作，若成功将从芯片公司转型为AI平台公司。这对整个AI行业都将产生深远影响。',
        
        'H100 prices are melting': 'GPU市场出现新动向。尽管外界预期价格下跌，H100却逆势上涨。这一现象背后是AI算力需求的持续爆发，大型模型训练对高端GPU的依赖程度超出市场预期。',
        
        'Everything is CLI': 'Latent Space深度分析一切皆为CLI的趋势。从代码生成到自动化工作流，命令行正在成为AI时代的新入口。这个变化反映了开发者对效率和控制的追求，也预示着AI工具的新方向，值得关注。',
        
        'Exponential View': 'Exponential View深入分析AI如何重塑工作方式。从自动化办公到决策流程，AI正在改变传统的工作模式。这篇文章探讨了AI工具在实际工作中的应用，以及它们如何帮助提高效率的同时保持人性化。',
        
        'Last Week in AI': 'Last Week in AI每周精选AI领域重要进展，涵盖技术突破、产品发布和行业动态。帮你快速掌握AI发展趋势，值得关注。',
        
        'Lex Fridman': 'Lex Fridman播客持续邀请AI领域顶尖人物对话，深度探讨技术前沿与人类未来。每期节目都是一场思想盛宴，对于关注AI发展的人来说不容错过。',
        
        "Lenny's": "Lenny's Newsletter专注于产品与增长领域，分享实用洞察与案例分析。对于产品经理和创业者来说是必读内容，每周更新，干货满满。",
        
        # 其他新闻
        'Stanford': '斯坦福大学最新研究测试了Claude、ChatGPT、Gemini等主流AI模型，发现它们在提供个人建议时普遍存在过度肯定的问题。这项涉及1127名参与者的研究在Hacker News引发521条评论激辩，AI的谄媚指数远超预期。有人认为这是AI的安全本能，也有人担忧长期被AI夸奖会削弱用户的判断力。这个话题没有标准答案，但值得每个人思考。',
        
        'Bluesky': '去中心化社交平台Bluesky正式推出AI产品Attie，用户可以用自然语言描述感兴趣的内容，AI会自动抓取整合。与Meta、X等巨头全面拥抱AI聊天功能不同，Bluesky选择了小而专的路线，用AI解决信息过载，而非做一个万能助手。这种务实的设计思路值得其他AI产品学习。',
        
        'Miasma': 'GitHub上出现了一个引发热议的开源工具Miasma，它能让AI爬虫陷入无限循环的虚假内容陷阱。随着AI公司疯狂抓取网络数据训练模型，内容创作者开始反击。支持者称这是创作者的正当防卫，批评者担忧它会误伤正常搜索引擎。AI时代的内容战争正在悄然升级。',
        
        'Sheet Ninja': 'Sheet Ninja让Google Sheets直接当CRUD后端，不需要服务器和数据库，一个Google账号加一个表格就能实现完整的增删改查功能。目标用户是不关心架构只想快速出活的程序员。它反映了编程门槛正在急剧下降的趋势，值得关注。',
        
        'GitLab': 'GitLab创始人Sytse一边与癌症抗争，一边继续经营公司。他将化疗与工作结合，在病床上参加董事会会议。Sytse说工作让我保持清醒，让我感觉自己在做有意义的事。这种用工作对抗命运的态度引发关于工作与生活平衡的思考，令人动容。',
        
        'SUN': 'a16z最新一期Speedrun加速营毕业项目SUN在Product Hunt亮相，本期主题围绕AI Native应用。这批项目普遍重视隐私计算和本地部署能力，似乎在回应用户对数据安全的担忧。AI创业潮正在从通用大模型向垂直应用加隐私优先快速转向。',
        
        'OneUsefulThing': 'One Useful Thing探讨AI产品在代理时代的应用策略，帮助用户理解如何在不同场景下选择合适的AI工具。内容实用且具有前瞻性，值得一读。',
        
        'Karpathy': 'Karpathy Loop探讨AI推理中的循环问题。当AI陷入重复思考时如何突破？这个话题对于理解大模型的局限性至关重要，也引发了关于AI思维链优化的讨论。',
        
        'Stripe': 'Stripe工程师分享了如何用AI代理每周自动处理1300个PR。从Slack reaction触发到代码审查，AI正在彻底改变传统开发流程。这个案例展示了AI代理在工程实践中的巨大潜力。',
        
        'Superhuman': 'Superhuman推出的AI代理功能让写作变得更透明高效。通过AI辅助，用户可以更专注于创意本身，而非被繁琐的编辑工作拖累。这种AI增强人的工作方式正在成为新的趋势。',
        
        'xAI': 'xAI的Colossus2数据中心正式投入使用，这是全球首个千兆瓦级别的AI训练设施。马斯克表示这将为Grok大模型提供前所未有的算力支持，AI训练正式进入兆瓦时代。',
        
        'Huawei': '华为昇腾芯片进入量产阶段，但HBM内存供应成为最大瓶颈。在美国制裁背景下，中国AI芯片产业正在寻求突破，昇腾的表现值得持续关注。',
        
        'JetBrains': 'JetBrains推出AI编排平台，帮助开发者更高效地管理和调度AI代理。这个平台可以将多个AI工具串联成完整的工作流，大幅提升开发效率，值得关注。',
        
        'Chroma': 'Chroma发布20B参数检索模型，专为多跳检索和上下文管理设计。这个模型可以更好地理解和处理复杂查询，为RAG应用提供更精准的支持，值得关注。',
        
        'GuideYou': 'GuideYou是一款AI驱动的旅行规划助手，能够根据用户偏好和预算自动生成个性化行程。与传统旅行APP不同，它更注重深度体验而非打卡式旅游。',
        
        'Pensieve': 'Pensieve是一款AI记忆管理工具，帮助用户更好地组织和检索信息。随着AI助手变得越来越强大，如何有效管理上下文信息成为关键问题。Pensieve的出现填补了这一空白。',
        
        # 新增新闻
        'Pixel 10a': '谷歌Pixel 10a取消摄像头凸起设计，这一决定获得了用户广泛好评。分析师认为这是谷歌在手机设计上的重大转变，放弃了激进的摄像头升级，转而追求更平衡的外观设计。',
        
        'YouTube CEO': 'YouTube CEO在最新采访中表示，最优秀的创作者永远不会离开这个平台。他强调YouTube为创作者提供了最完善的变现工具和观众群体，这是其他平台无法比拟的优势。',
        
        'Project Hail Mary': '科幻电影Project Hail Mary成为Amazon MGM出品的有史以来票房最高的影片。这部电影的成功证明了科幻题材在流媒体时代的持久吸引力。',
        
        'Sora shutdown': 'OpenAI关闭Sora视频生成服务，引发行业震动。分析师认为这可能是AI视频领域的一个重要转折点，提醒各大公司需要更加重视内容安全和商业可行性。',
        
        'TechCrunch Mobility': 'TechCrunch Mobility报道了一起特殊事件： robotaxi在遇到突发状况时自动呼叫911。这一事件再次将自动驾驶安全性问题推向风口浪尖。',
        
        'Coding Agents': '编程代理工具正在让自由软件重新获得关注。这些AI工具降低了代码贡献的门槛，让更多非专业开发者能够参与开源项目。',
        
        'ChatGPT Won\'t Let': 'ChatGPT新增安全机制，在读取用户React状态之前会阻止输入。这一更新引发了开发者社区的讨论，有人欢迎更强的隐私保护，也有人抱怨操作变得繁琐。',
        
        'Cognitive Dark Forest': '一篇关于AI认知局限的长文引发热议。作者指出大语言模型可能陷入认知黑暗森林，无法真正理解世界的复杂性。这一观点获得了AI研究者的广泛讨论。',
        
        'Voyager 1': 'NASA确认Voyager 1飞船仅靠69KB内存和磁带机仍在正常运行。这一工程奇迹让人们对上世纪70年代的技术水平惊叹不已。',
        
        'Parallel Code': 'Parallel Code是一款新型并行代码生成工具，能够同时处理多个代码片段。它代表了编程辅助工具的新方向，值得关注。',
        
        'CodingPrep': 'CodingPrep是一款专注于编程面试的准备工具，提供模拟面试和即时反馈功能。它帮助求职者更高效地准备技术面试。',
        
        'Peopling': 'Peopling是一款社交网络分析工具，能够帮助用户理解社交关系网络。它在研究人员和营销人员中获得广泛应用。',
    }
    
    for key, content in zh_map.items():
        if key.lower() in clean_title.lower():
            return content
    
    # 默认生成中文摘要
    return f'{clean_title}。这个消息值得关注，业界正在密切关注其后续发展，建议持续关注相关动态。'[:200] + '...'

def upload_qrcode(token):
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
    sources = ['HackerNews', 'TechCrunch', 'ProductHunt', 'TheSequence', 
              'LatentSpace', 'ExponentialView', 'LexFridman', 'LennysNewsletter',
              'LastWeekinAI', 'OneUsefulThing']
    news_data = {}
    for source in sources:
        cur.execute('SELECT * FROM news WHERE source=? ORDER BY score DESC, date DESC LIMIT 5', (source,))
        rows = cur.fetchall()
        if rows:
            filtered = [r for r in rows if r['title'] not in history]
            if filtered:
                news_data[source] = [dict(r) for r in filtered]
    conn.close()
    return news_data

def select_hot_topic(news_data):
    hot_keywords = ['stanford', 'openai', 'anthropic', 'google', 'nvidia', 'meta', 'apple', 
                    'the sequence', 'exponential', 'last week', 'lex fridman',
                    '炸锅', '突发', '重磅', '爆火', '震惊']
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
            # H100/GPU 加更高分
            if 'h100' in title_lower or 'gpu' in title_lower:
                score += 30  # 提高优先级
            if 'latentspace' in source.lower():
                score += 5   # LatentSpace来源加一点分
            score += item.get('score', 0)
            if score > best_score:
                best_score = score
                best = item
                best_source = source
    return best, best_source

def generate_dynamic_title(item):
    """生成动态吸睛标题"""
    title = item['title'].lower()
    
    # 炸锅风格 - 更多关键词
    if any(kw in title for kw in ['zuckerberg', 'musk', 'meta', 'openai', 'nvidia', 'google', 'anthropic',
                                    'the sequence', 'exponential', 'last week', 'lex fridman', 'h100', 'gpu']):
        prefix = random.choice(['炸锅', '突发', '重磅', '曝料', '刚刚'])
        return f'{prefix}！{translate_title(item["title"])}'
    
    # 默认风格
    return translate_title(item['title'])

def generate_content(news_data, hot_item=None, hot_source=None, qrcode_url=''):
    now = datetime.datetime.now()
    date_str = now.strftime('%Y.%m.%d')
    hour = now.hour
    edition = '早报' if hour < 12 else '午报' if hour < 18 else '晚报'
    html = ''
    
    # 热点聚焦模块 - 白色背景 + 橙色边框，140字摘要放在里面
    if hot_item:
        hot_content = get_content(hot_item['title'])
        html += f'''<p style="margin: 20px 15px; padding: 20px; background: #fff; border: 2px solid #ff6600; border-radius: 8px; text-align: center;">
  <strong style="font-size: 14px; color: #555; line-height: 1.8;">{hot_content}</strong>
</p>'''
    
    # 整合SubStack来源为一个模块（不含LatentSpace，让它作为独立平台显示H100）
    substack_sources = ['ExponentialView', 'LexFridman', 
                         'LennysNewsletter', 'LastWeekinAI', 'OneUsefulThing']
    substack_items = []
    for s in substack_sources:
        if s in news_data:
            substack_items.extend(news_data[s])
            del news_data[s]
    # LatentSpace 和 TheSequence 保留为独立平台
    
    # 平台顺序 - SubStack模块置顶
    platforms = list(news_data.keys())
    # SubStack模块始终置顶
    platforms = ['SubStack'] + [p for p in platforms if p != 'SubStack']
    
    # 平台配置 - 不同平台不同背景色+左侧竖条+彩色标题（统一风格）
    configs = {
        'HackerNews': {'name': 'Hacker News', 'bg': '#fff3e0', 'color': '#e65100', 'border': '#e65100'},
        'ProductHunt': {'name': 'Product Hunt', 'bg': '#fce4ec', 'color': '#c2185b', 'border': '#c2185b'},
        'TechCrunch': {'name': 'TechCrunch', 'bg': '#e8f5e9', 'color': '#2e7d32', 'border': '#2e7d32'},
        'TheSequence': {'name': 'The Sequence', 'bg': '#f3e5f5', 'color': '#6a1b9a', 'border': '#6a1b9a'},
        'LatentSpace': {'name': 'Latent Space', 'bg': '#e1f5fe', 'color': '#0288d1', 'border': '#0288d1'},
        'SubStack': {'name': 'SubStack 精选', 'bg': '#fff8e1', 'color': '#f57c00', 'border': '#f57c00'},
    }
    
    # 动态调整：热门话题对应的模块置顶
    if hot_source and hot_source in platforms:
        platforms.remove(hot_source)
        platforms.insert(0, hot_source)
    
    for source in platforms:
        if source not in news_data and source != 'SubStack':
            continue
        # SubStack从substack_items获取
        if source == 'SubStack':
            items = substack_items[:4]
        else:
            items = news_data.get(source, [])[:4]
        
        cfg = configs.get(source, {'name': source, 'bg': '#f5f5f5', 'color': '#666', 'border': '#666'})
        label = f'【置顶】{cfg["name"]}' if source == hot_source else cfg['name']
        
        # 子标题：背景色+左侧竖条颜色与平台一致+彩色标题
        html += f'''<p style="margin: 25px 0 10px 0; padding: 12px 15px; background: {cfg['bg']}; border-left: 4px solid {cfg['border']}; border-radius: 4px;">
  <strong style="font-size: 15px; color: {cfg['color']};">{label}</strong>
</p>'''
        
        for i, item in enumerate(items):
            title = translate_title(item['title'])
            content = get_content(item['title'])
            img_url = get_topic_image(item['title'])
            html += f'<p style="margin: 12px 0 5px 0; font-size: 15px; color: #1a1a1a;"><strong>{title}</strong></p>'
            html += f'<p style="margin: 0; font-size: 14px; color: #555; line-height: 1.8;"><img src="{img_url}" style="width: 100%; max-width: 400px; border-radius: 6px; margin-bottom: 10px;" alt="cover">{content}</p>'
            # 每个区块都有虚线分隔
            if i < len(items) - 1:
                html += '<p style="margin: 12px 0; border-top: 1px dashed #ddd;"></p>'
    
    # 结尾 - 不显示二维码
    html += f'<p style="text-align: center; margin-top: 30px; font-size: 12px; color: #999;">© {now.year} grepAI | 认真做内容</p>'
    
    return html, date_str, edition

def publish():
    print('='*50)
    print('AI News 发布')
    print(f'时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*50)
    
    token = get_token()
    print('Token获取成功')
    
    # 上传二维码（用于文章底部）
    thumb_id, thumb_url = upload_qrcode(token)
    print('二维码上传成功')
    
    # 选择最热话题作为封面图
    news_data = get_news()
    total = sum(len(items) for items in news_data.items())
    print(f'获取到 {total} 条新闻，覆盖 {len(news_data)} 个平台')
    
    if not news_data:
        print('没有新闻')
        return False
    
    hot_item, hot_source = select_hot_topic(news_data)
    hot_title = translate_title(hot_item['title']) if hot_item else ''
    print(f'热门话题: {hot_title}')
    
    content, date_str, edition = generate_content(news_data, hot_item, hot_source, thumb_url)
    
    # 文章标题 = 动态标题（如：炸锅！The Sequence上周AI回顾...）
    title = generate_dynamic_title(hot_item) if hot_item else f'{date_str} 全球AI科技{edition}'
    print(f'文章标题: {title}')
    
    # 获取封面图（与标题匹配）
    cover_url = get_topic_image(hot_item['title']) if hot_item else IMAGE_MAP['default']
    cover_id = thumb_id  # 默认使用二维码
    
    # 下载并上传封面图到微信服务器
    r = requests.get(cover_url, timeout=10)
    if r.status_code == 200:
        img = Image.open(io.BytesIO(r.content)).convert('RGB')
        img = img.resize((900, 383), Image.LANCZOS)
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            img.save(f.name, 'JPEG', quality=85)
            path = f.name
        try:
            with open(path, 'rb') as f:
                resp = requests.post(
                    f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image',
                    files={'media': f}
                )
            result = resp.json()
            if 'media_id' in result:
                cover_id = result['media_id']
                print(f'封面图上传成功')
        finally:
            os.unlink(path)
    
    data = {
        'articles': [{
            'title': title,
            'author': 'grepAI',
            'content': content,
            'digest': hot_title if hot_title else title,
            'thumb_media_id': cover_id,
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
        print(f'发布成功!')
        print(f'media_id: {media_id}')
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
        print(f'热门: {result["hot"]}')