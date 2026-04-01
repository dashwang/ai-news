#!/usr/bin/env python3
"""
公众号发布脚本 - 2026年3月29日最新版
格式要求：
1. 热点聚焦模块 - 白色背景 + 橙色边框
2. 四平台各自不同颜色
3. 中文标题 + 140字+摘要
4. 标题加粗
5. 虚线分割
6. 无开场白
7. 无emoji
8. 自动配图
9. SubStack整合为一个模块
10. 全自动实时翻译
"""
import requests, json, datetime, os, sqlite3, io, tempfile
from PIL import Image

# Free translation API (MyMemory)
def translate_to_zh(text):
    """使用免费翻译API将英文翻译为中文"""
    if not text or not text.strip():
        return text
    
    # 如果文本已经是中文（包含中文字符），直接返回
    if any('\u4e00' <= c <= '\u9fff' for c in text):
        return text
    
    try:
        # 使用 MyMemory 免费翻译 API
        url = "https://api.mymemory.translated.net/get"
        params = {
            'q': text,
            'langpair': 'en|zh-CN'
        }
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        if result.get('responseStatus') == 200:
            translated = result.get('responseData', {}).get('translatedText', '')
            if translated:
                return translated
    except Exception as e:
        print(f"翻译API调用失败: {e}")
    
    # API失败时fallback到简单处理
    return f"【AI快讯】{text[:40]}..."

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
        'SXSW rebounds': 'SXSW回归：顶级创业者和VC社交盛会',
        'Elon Musk last co-founder': '马斯克最后一位联合创始人离开xAI',
        'Overestimation of microplastics': '研究警告：实验室手套可能导致数据失准',
        'USB cable tester': '完美USB线缆测试器真的存在吗',
        'TSA lines': '机场安检大排长龙催生排队中介新职业',
        'Karpathy Loop': 'Karpathy Loop解决AI推理循环问题',
        'LWiAI Podcast': '上周AI播客：Nemotron 3、xAI重生、Anthropic诉讼',
        'Authorship Launches': 'Superhuman推出AI写作代理功能',
        'Partner Agents': 'Superhuman推出合作伙伴AI代理',
        'Guide to Which AI': 'AI代理时代如何选择合适的AI工具',
        'Shape of the Thing': 'AI产品的形态正在改变',
        'GuideYou': 'GuideYou AI旅行规划助手',
        'Parallel Code': 'Parallel Code并行代码生成工具',
        'Pensieve': 'Pensieve AI记忆管理工具',
        'Jensen Huang': '黄仁勋对话LL COOL J：AI革命的幕后推手',
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
        'The Sequence Radar': 'The Sequence上周AI回顾压缩语音与算力',
        'The Sequence Opinion': 'The Sequence NVIDIA正在构建AI操作系统',
        'H100 prices': 'GPU市场异动H100价格逆势上涨',
        'Everything is CLI': '一切皆为CLI的时代正在到来',
        'Exponential View': 'Exponential View AI如何重塑工作方式',
        'Last Week in AI': 'Last Week in AI上周AI重要进展回顾',
        'Lex Fridman': 'Lex Fridman AI领域深度对话',
        "Lenny's Newsletter": "Lenny's Newsletter产品与增长洞察",
        'LWiAI Podcast #237': '上周AI播客Nemotron 3、xAI重生、Anthropic诉讼',
        'OneUsefulThing': 'One Useful Thing AI产品与增长思考',
        'The Shape': 'AI产品的形态正在改变',
        '#494': 'Lex Fridman对话黄仁勋NVIDIA的AI革命',
        '#493': 'Lex Fridman对话Jeff Kaplan魔兽世界与游戏未来',
        '#492': 'Lex Fridman对话Rick Beato吉他与音乐的未来',
        'From skeptic': '从怀疑者到信徒OpenClaw改变我的工作方式',
        'How Stripe': 'Stripe用AI代理每周自动处理1300个PR',
        'Community': '社区智慧当AI速度超越产品策略',
    }
    
    for key, zh in zh_map.items():
        if key.lower() in clean_title.lower():
            return zh
    
    # 使用实时翻译
    return translate_to_zh(clean_title)

def get_content(en_title):
    """翻译内容为中文，清理emoji"""
    clean_title = en_title
    for char in ['🔮', '🔥', '💡', '📱', '📚', '🎉', '❤️', '👍', '✨', '🚨', '📰', '🎊', '🧠']:
        clean_title = clean_title.replace(char, '').strip()
    
    zh_map = {
        'Zuckerberg': '据TechCrunch报道，Meta CEO扎克伯格曾主动给马斯克发短信，提议帮助政府效率部DOGE的工作。这条消息在硅谷引发各种解读，有人认为这是向权力靠拢，也有人认为只是礼貌性示好。无论动机如何，AI圈大佬们正在以各种方式与权力产生交集，值得持续关注。',
        
        'Stanford': '斯坦福大学最新研究测试了Claude、ChatGPT、Gemini等主流AI模型，发现它们在提供个人建议时普遍存在过度肯定的问题。这项涉及1127名参与者的研究在Hacker News引发521条评论激辩，AI的谄媚指数远超预期。有人认为这是AI的安全本能，也有人担忧长期被AI夸奖会削弱用户的判断力。这个话题没有标准答案，但值得每个人思考。',
        
        'Bluesky': '去中心化社交平台Bluesky正式推出AI产品Attie，用户可以用自然语言描述感兴趣的内容，AI会自动抓取整合。与Meta、X等巨头全面拥抱AI聊天功能不同，Bluesky选择了小而专的路线，用AI解决信息过载，而非做一个万能助手。这种务实的设计思路值得其他AI产品学习。',
        
        'Miasma': 'GitHub上出现了一个引发热议的开源工具Miasma，它能让AI爬虫陷入无限循环的虚假内容陷阱。随着AI公司疯狂抓取网络数据训练模型，内容创作者开始反击。支持者称这是创作者的正当防卫，批评者担忧它会误伤正常搜索引擎。AI时代的内容战争正在悄然升级。',
        
        'Sheet Ninja': 'Sheet Ninja让Google Sheets直接当CRUD后端，不需要服务器和数据库，一个Google账号加一个表格就能实现完整的增删改查功能。目标用户是不关心架构只想快速出活的程序员。它反映了编程门槛正在急剧下降的趋势，值得关注。',
        
        'GitLab': 'GitLab创始人Sytse一边与癌症抗争，一边继续经营公司。他将化疗与工作结合，在病床上参加董事会会议。Sytse说工作让我保持清醒，让我感觉自己在做有意义的事。这种用工作对抗命运的态度引发关于工作与生活平衡的思考，令人动容。',
        
        'SUN': 'a16z最新一期Speedrun加速营毕业项目SUN在Product Hunt亮相，本期主题围绕AI Native应用。这批项目普遍重视隐私计算和本地部署能力，似乎在回应用户对数据安全的担忧。AI创业潮正在从通用大模型向垂直应用加隐私优先快速转向。',
        
        'Everything is CLI': 'Latent Space深度分析一切皆为CLI的趋势。从代码生成到自动化工作流，命令行正在成为AI时代的新入口。这个变化反映了开发者对效率和控制的追求，也预示着AI工具的新方向，值得关注。',
        
        'NVIDIA': 'TechCrunch报道NVIDIA正在构建AI的操作系统，一个统一软件层协调不同AI模型和数据源。分析师认为这是NVIDIA最具战略意义的动作，若成功将从芯片公司转型为AI平台公司。这对整个AI行业都将产生深远影响。',
        
        'H100': 'GPU市场出现新动向。尽管外界预期价格下跌，H100却逆势上涨。这一现象背后是AI算力需求的持续爆发，大型模型训练对高端GPU的依赖程度超出市场预期。',
        
        'Exponential View': 'Exponential View深入分析AI如何重塑工作方式。从自动化办公到决策流程，AI正在改变传统的工作模式。这篇文章探讨了AI工具在实际工作中的应用，以及它们如何帮助提高效率的同时保持人性化。',
        
        'The Sequence': 'The Sequence回顾上周AI重要进展：压缩技术突破、语音模型进化、算力格局变化。本期涵盖技术突破、产品发布和行业洞见，帮你快速了解AI发展动态。',
        
        'Last Week in AI': 'Last Week in AI每周精选AI领域重要进展，涵盖技术突破、产品发布和行业动态。帮你快速掌握AI发展趋势，值得关注。',
        
        'Lex Fridman': 'Lex Fridman播客持续邀请AI领域顶尖人物对话，深度探讨技术前沿与人类未来。每期节目都是一场思想盛宴，对于关注AI发展的人来说不容错过。',
        
        "Lenny's": "Lenny's Newsletter专注于产品与增长领域，分享实用洞察与案例分析。对于产品经理和创业者来说是必读内容，每周更新，干货满满。",
        
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
    }
    
    for key, content in zh_map.items():
        if key.lower() in clean_title.lower():
            return content
    
    # 使用实时翻译摘要
    return translate_to_zh(clean_title)

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
    sources = ['HackerNews', 'TechCrunch', 'ProductHunt', 'TheSequence', 'Superhuman', 'SemiAnalysis', 'TechMonitor', 'MarkTechPost', 'AnalyticsVidhya', 'OpenAIBlog', 'GoogleAI', 'MicrosoftAI', 'NVIDIA',  
              'LatentSpace', 'ExponentialView', 'LexFridman', 'LennysNewsletter',
              'LastWeekinAI', 'OneUsefulThing']
    news_data = {}
    for source in sources:
        cur.execute('SELECT * FROM news WHERE source=? ORDER BY score DESC, date DESC LIMIT 8', (source,))
        rows = cur.fetchall()
        if rows:
            filtered = [r for r in rows if r['title'] not in history]
            if filtered:
                news_data[source] = [dict(r) for r in filtered]
    conn.close()
    return news_data

def select_hot_topic(news_data):
    hot_keywords = ['stanford', 'openai', 'anthropic', 'google', 'nvidia', 'meta', 'apple', 
                    'billion', 'funding', 'musk', 'zuckerberg', 'altman', 'llm', 'model',
                    '炸锅', '突发', '重磅']
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
    
    # 整合SubStack来源为一个模块
    substack_sources = ['TheSequence', 'LatentSpace', 'ExponentialView', 'LexFridman', 
                         'LennysNewsletter', 'LastWeekinAI', 'OneUsefulThing']
    substack_items = []
    for s in substack_sources:
        if s in news_data:
            substack_items.extend(news_data[s])
            del news_data[s]
    
    # 平台顺序 - 置顶的放第一
    platforms = list(news_data.keys())
    if hot_source and hot_source in platforms:
        platforms.remove(hot_source)
        platforms.insert(0, hot_source)
    
    # 平台配置
    configs = {
        'HackerNews': {'color': '#e65100', 'bg': '#fff3e0', 'name': 'Hacker News'},
        'ProductHunt': {'color': '#c2185b', 'bg': '#fce4ec', 'name': 'Product Hunt'},
        'TechCrunch': {'color': '#2e7d32', 'bg': '#e8f5e9', 'name': 'TechCrunch'},
    }
    
    for source in platforms:
        if source not in news_data:
            continue
        items = news_data[source]
        cfg = configs.get(source, {'color': '#666', 'bg': '#f5f5f5', 'name': source})
        label = f'【置顶】{cfg["name"]}' if source == hot_source else cfg['name']
        
        html += f'''<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: {cfg['bg']}; border-radius: 8px; border-left: 4px solid {cfg['color']}; text-align: center;">
  <strong style="font-size: 16px; color: {cfg['color']};">{label}</strong>
</p>'''
        
        for item in items[:8]:
            title = translate_title(item['title'])
            content = get_content(item['title'])
            img_url = get_topic_image(item['title'])
            html += f'''<p style="margin: 15px 0 5px 0;"><strong style="font-size: 15px; color: #1a1a1a;"><b>{title}</b></strong></p>
<p style="margin: 0; font-size: 14px; color: #555; line-height: 1.8; text-align: justify;"><img src="{img_url}" style="width: 100%; max-width: 400px; border-radius: 8px; margin-bottom: 10px;" alt="cover">{content}</p>
<p style="margin: 10px 0; border-top: 1px dashed #e0e0e0;"></p>'''
    
    # SubStack整合模块
    if substack_items:
        html += '''<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: #fff8e1; border-radius: 8px; border-left: 4px solid #f57c00; text-align: center;">
  <strong style="font-size: 16px; color: #f57c00;">SubStack 精选</strong>
</p>'''
        for item in substack_items[:8]:
            title = translate_title(item['title'])
            content = get_content(item['title'])
            img_url = get_topic_image(item['title'])
            html += f'''<p style="margin: 15px 0 5px 0;"><strong style="font-size: 15px; color: #1a1a1a;"><b>{title}</b></strong></p>
<p style="margin: 0; font-size: 14px; color: #555; line-height: 1.8; text-align: justify;"><img src="{img_url}" style="width: 100%; max-width: 400px; border-radius: 8px; margin-bottom: 10px;" alt="cover">{content}</p>
<p style="margin: 10px 0; border-top: 1px dashed #e0e0e0;"></p>'''
    
    # 结尾 - 二维码铺满屏幕宽度，保持原始比例
    html += f'''<div style="width: 100%; margin-top: 20px; text-align: center;">
  <img src="{qrcode_url}" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 0;" alt="qrcode">
</div>
<p style="text-align: center; margin-top: 15px; font-size: 14px; color: #666;">扫码关注「grepAI」<br>每天早上自动送达</p>
<p style="text-align: center; margin-top: 12px; font-size: 11px; color: #ccc;">© {now.year} grepAI | 认真做内容</p>'''
    
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
    
    # 文章标题 = 动态标题（如：炸锅！扎克伯格主动联系马斯克）
    title = hot_title if hot_title else f'{date_str} 全球AI科技{edition}'
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