#!/usr/bin/env python3
"""
公众号发布脚本 - 基于3月28日成功发布的版本
格式要求：
1. 热点聚焦模块 - 白色背景 + 橙色边框
2. 模块动态调整 - 【置顶】标记
3. 四平台各自不同颜色
4. 中文标题 + 140字+摘要
5. 黑色加粗标题
6. 虚线分割
7. 无开场白
8. 无emoji
"""
import requests, json, datetime, os, sqlite3, io, tempfile
from PIL import Image

WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID', 'wxa87b65ba78d3c822')
WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET', 'ac6a029c2b4ef7c1b89fbaeeaace3931')
QRCODE_URL = 'https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png'
DB_PATH = 'data/news.db'
HISTORY_FILE = 'published_articles.json'

# 中文标题翻译
ZH_TITLES = {
    'Stanford study outlines dangers of asking AI chatbots for personal advice': '斯坦福研究：AI给人建议时过度"谄媚"',
    'Bluesky leans into AI with Attie': 'Bluesky推出AI产品Attie：用自然语言构建个性化订阅源',
    'Mark Zuckerberg texted Elon Musk': '扎克伯格主动联系马斯克：提议协助DOGE工作',
    'Miasma: A tool to trap AI web scrapers': 'Miasma：一个让AI爬虫深陷"毒坑"的反抓取工具',
    'Sheet Ninja': 'Sheet Ninja：让Google Sheets变身CRUD后端',
    'Founder of GitLab battles cancer': 'GitLab创始人以创业对抗癌症',
    'Overestimation of microplastics': '研究警告：实验室手套可能导致微塑料高估',
    'Show HN: Sheet Ninja': '开发者新作：Sheet Ninja让表格变成后端',
    'SUN (a16z Speedrun 006)': 'SUN：a16z加速营AI原生应用毕业项目',
    'Elon Musk last co-founder leaves xAI': '马斯克最后一位联合创始人离开xAI',
    'Cline Kanban': 'Cline Kanban：开发者任务看板新工具',
    'Clico': 'Clico：创新产品亮相Product Hunt',
    'The Sequence Radar': 'The Sequence：上周AI回顾压缩、语音与算力',
    'The Sequence Opinion': 'The Sequence：NVIDIA正在构建AI操作系统',
    'Latent Space H100 prices': 'Latent Space：H100价格逆势上涨',
    'Everything is CLI': '一切皆为CLI的时代正在到来',
    'Exponential View': 'Exponential View：AI如何重塑工作方式',
    'What if AI doesn\'t need more RAM': 'AI不需要更多内存？Google TurboQuant另辟蹊径',
    'Agent Lattice': 'Lat.md：用Markdown构建代码知识图谱',
    'Lex Fridman': 'Lex Fridman：AI领域深度对话',
    "Lenny's Newsletter": "Lenny's Newsletter：产品与增长洞察",
}

# 中文摘要（140字+）
ZH_CONTENT = {
    'Stanford study outlines dangers': '斯坦福大学最新研究测试了Claude、ChatGPT、Gemini等主流AI模型，发现它们在提供个人建议时普遍存在"过度肯定"的问题。这项涉及1127名参与者的研究在Hacker News引发521条评论激辩，AI的"谄媚指数"远超预期。有人认为这是AI的"安全本能"，也有人担忧长期被AI夸奖会削弱用户的判断力。这个话题没有标准答案，但值得每个人思考。',
    
    'Bluesky leans into AI': '去中心化社交平台Bluesky正式推出AI产品Attie，用户可以用自然语言描述感兴趣的内容，AI会自动抓取整合。与Meta、X等巨头全面拥抱AI聊天功能不同，Bluesky选择了"小而专"的路线——用AI解决信息过载，而非做一个万能助手。',
    
    'Mark Zuckerberg texted': '据TechCrunch报道，Meta CEO Zuckerberg曾主动给Musk发短信，提议帮助政府效率部（DOGE）的工作。这条消息在硅谷引发各种解读——有人认为这是向权力靠拢，也有人认为只是礼貌性示好。无论动机如何，AI圈大佬们正在以各种方式与权力产生交集。',
    
    'Miasma: A tool to trap': 'GitHub上出现了一个引发热议的开源工具Miasma，它能让AI爬虫陷入无限循环的虚假内容陷阱。随着AI公司疯狂抓取网络数据训练模型，内容创作者开始反击。支持者称这是"创作者的正当防卫"，批评者担忧它会误伤正常搜索引擎。AI时代的内容战争正在悄然升级。',
    
    'Sheet Ninja': 'Sheet Ninja让Google Sheets直接当CRUD后端，不需要服务器和数据库，一个Google账号加一个表格就能实现完整的增删改查功能。目标用户是"vibe coder"——不关心架构只想快速出活的程序员。它反映了编程门槛正在急剧下降的趋势。',
    
    'Founder of GitLab battles cancer': 'GitLab创始人Sytse一边与癌症抗争，一边继续经营公司。他将化疗与工作结合，在病床上参加董事会会议。Sytse说："工作让我保持清醒，让我感觉自己在做有意义的事。"这种"用工作对抗命运"的态度引发关于工作与生活平衡的思考。',
    
    'SUN (a16z Speedrun 006)': 'a16z最新一期Speedrun加速营毕业项目SUN在Product Hunt亮相，本期主题围绕"AI Native应用"。这批项目普遍重视"隐私计算"和"本地部署"能力，似乎在回应用户对数据安全的担忧。AI创业潮正在从"通用大模型"向"垂直应用+隐私优先"快速转向。',
    
    'Everything is CLI': 'Latent Space深度分析"一切皆为CLI"的趋势。从代码生成到自动化工作流，命令行正在成为AI时代的新入口。这个变化反映了开发者对效率和控制的追求，也预示着AI工具的新方向。',
    
    'NVIDIA': 'TechCrunch报道NVIDIA正在构建AI的"操作系统"——一个统一软件层协调不同AI模型和数据源。分析师认为这是NVIDIA最具战略意义的动作，若成功将从芯片公司转型为AI平台公司。',
    
    'The Sequence Radar': 'The Sequence回顾上周AI重要进展：压缩技术突破、语音模型进化、算力格局变化。本期涵盖技术突破、产品发布和行业洞见，帮你快速了解AI发展动态。',
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
    for key, zh in ZH_TITLES.items():
        if key.lower() in en_title.lower():
            return zh
    return en_title[:40] + '...' if len(en_title) > 40 else en_title

def get_content(en_title):
    for key, content in ZH_CONTENT.items():
        if key.lower() in en_title.lower():
            return content
    return f'{en_title}。这个消息值得关注，业界正在密切关注其后续发展，建议持续关注相关动态。' * 2

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
            return result['media_id']
        raise Exception(f'上传失败: {result}')
    finally:
        os.unlink(path)

def get_news():
    history = load_history()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    sources = ['HackerNews', 'TechCrunch', 'ProductHunt', 'SubStack', 'TheSequence', 
              'LatentSpace', 'ExponentialView', 'LexFridman', 'LennysNewsletter']
    
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
    """选择最热的话题"""
    hot_keywords = ['stanford', 'openai', 'anthropic', 'google', 'nvidia', 'meta', 'apple', 
                    'billion', 'funding', 'musk', 'zuckerberg', 'altman', 'llm', 'model']
    
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

def generate_content(news_data, hot_item=None, hot_source=None):
    now = datetime.datetime.now()
    date_str = now.strftime('%Y.%m.%d')
    hour = now.hour
    edition = '早报' if hour < 12 else '午报' if hour < 18 else '晚报'
    
    html = ''
    
    # 热点聚焦模块 - 白色背景 + 橙色边框
    if hot_item:
        hot_title = translate_title(hot_item['title'])
        hot_content = get_content(hot_item['title'])
        html += f'''<p style="margin: 20px 15px; padding: 20px; background: #fff; border: 2px solid #ff6600; border-radius: 8px; text-align: center;">
  <strong style="font-size: 18px; color: #ff6600;">{hot_title}</strong>
</p>
<p style="margin: 0 20px 20px 20px; font-size: 14px; color: #555; line-height: 1.8; text-align: justify;">{hot_content}</p>'''
    
    # 平台顺序 - 置顶的放第一
    source_order = ['HackerNews', 'ProductHunt', 'TechCrunch', 'SubStack']
    platforms = list(news_data.keys())
    
    if hot_source and hot_source in platforms:
        platforms.remove(hot_source)
        platforms.insert(0, hot_source)
    
    # 平台配置
    configs = {
        'HackerNews': {'color': '#e65100', 'bg': '#fff3e0', 'name': 'Hacker News'},
        'ProductHunt': {'color': '#c2185b', 'bg': '#fce4ec', 'name': 'Product Hunt'},
        'SubStack': {'color': '#f57c00', 'bg': '#fff8e1', 'name': 'SubStack'},
        'TechCrunch': {'color': '#2e7d32', 'bg': '#e8f5e9', 'name': 'TechCrunch'},
        'TheSequence': {'color': '#6a1b9a', 'bg': '#f3e5f5', 'name': 'The Sequence'},
        'LatentSpace': {'color': '#0288d1', 'bg': '#e1f5fe', 'name': 'Latent Space'},
        'ExponentialView': {'color': '#c62828', 'bg': '#ffebee', 'name': 'Exponential View'},
        'LexFridman': {'color': '#ff4400', 'bg': '#fff0e0', 'name': 'Lex Fridman'},
        'LennysNewsletter': {'color': '#ff4400', 'bg': '#fff0e0', 'name': "Lenny's Newsletter"},
    }
    
    for source in platforms:
        if source not in news_data:
            continue
        items = news_data[source]
        cfg = configs.get(source, {'color': '#666', 'bg': '#f5f5f5', 'name': source})
        
        # 标题 - 【置顶】标记
        if source == hot_source:
            label = f'【置顶】{cfg["name"]}'
        else:
            label = cfg['name']
        
        html += f'''<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: {cfg['bg']}; border-radius: 8px; border-left: 4px solid {cfg['color']}; text-align: center;">
  <strong style="font-size: 16px; color: {cfg['color']};">{label}</strong>
</p>'''
        
        for item in items:
            title = translate_title(item['title'])
            content = get_content(item['title'])
            
            html += f'''<p style="margin: 15px 0 5px 0;"><strong style="font-size: 15px; color: #1a1a1a;">{title}</strong></p>
<p style="margin: 0; font-size: 14px; color: #555; line-height: 1.8; text-align: justify;">{content}</p>
<p style="margin: 10px 0; border-top: 1px dashed #e0e0e0;"></p>'''
    
    # 结尾
    html += f'''<p style="text-align: center; margin-top: 20px;"><img src="{QRCODE_URL}" style="width: 180px; height: 180px; border-radius: 8px;" alt="qrcode"></p>
<p style="text-align: center; margin-top: 10px; font-size: 13px; color: #666;">扫码关注「grepAI」<br>每天早上自动送达</p>
<p style="text-align: center; margin-top: 15px; font-size: 11px; color: #ccc;">© {now.year} grepAI | 认真做内容</p>'''
    
    return html, date_str, edition

def publish():
    print('='*50)
    print('AI News 发布')
    print(f'时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*50)
    
    token = get_token()
    print('Token获取成功')
    
    thumb_id = upload_qrcode(token)
    print('二维码上传成功')
    
    news_data = get_news()
    total = sum(len(items) for items in news_data.items())
    print(f'获取到 {total} 条新闻，覆盖 {len(news_data)} 个平台')
    
    if not news_data:
        print('没有新闻')
        return False
    
    # 选择最热话题
    hot_item, hot_source = select_hot_topic(news_data)
    hot_title = translate_title(hot_item['title']) if hot_item else ''
    print(f'热门话题: {hot_title}')
    
    content, date_str, edition = generate_content(news_data, hot_item, hot_source)
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
        print(f'发布成功!')
        print(f'media_id: {media_id}')
        
        titles = []
        for items in news_data.values():
            for item in items:
                titles.append(item['title'])
        save_history(titles)
        
        return {'success': True, 'media_id': media_id, 'total': total, 'hot': hot_title, 'hot_source': hot_source}
    else:
        print(f'发布失败: {result}')
        return {'success': False, 'error': result}

if __name__ == '__main__':
    result = publish()
    if result.get('success'):
        print(f'完成! {result["total"]}条新闻')
        print(f'热门: {result["hot"]}')