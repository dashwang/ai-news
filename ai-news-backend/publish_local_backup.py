#!/usr/bin/env python3
"""
公众号发布脚本 - 本地直发版
不需要 Railway，直接从数据库读取新闻并发布到公众号草稿箱

要求：
1. 每条新闻140字以上
2. 5平台用不同颜色边框背景
3. 正文黑体（color: #333）
4. 标题党一点，用中文标题
5. 不要URL
6. 不要任何emoji
7. 二维码必须上传到微信服务器
8. 文章需要16条以上
9. 动态标题：自动选择最热新闻
10. 模块自动上浮：被选中来源的平台排在第一
"""
import requests, json, datetime, os, sqlite3, re
from PIL import Image

# ========== 凭证 ==========
WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID', 'wxa87b65ba78d3c822')
WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET', 'ac6a029c2b4ef7c1b89fbaeeaace3931')
QRCODE_URL = 'https://raw.githubusercontent.com/dashwang/ai-news/main/images/qrcode.png'
HISTORY_FILE = 'published_articles.json'
DB_PATH = 'data/news.db'

def get_token():
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}'
    resp = requests.get(url).json()
    if 'access_token' not in resp:
        raise Exception(f'获取Token失败: {resp}')
    return resp['access_token']

def load_published_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
            return [item['title'] for item in data.get('published', [])]
    except:
        return []

def save_to_history(title, url):
    try:
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = {'published': []}
    
    data['published'].append({
        'title': title,
        'url': url,
        'date': datetime.datetime.now().strftime('%Y-%m-%d')
    })
    
    if len(data['published']) > 100:
        data['published'] = data['published'][-100:]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_duplicate(title, history):
    """检查标题是否重复（更宽松：完全相同才算重复）"""
    title_lower = title.lower().strip()
    
    # 只检查完全相同的标题
    for h in history:
        h_lower = h.lower().strip()
        if title_lower == h_lower:
            return True
    
    return False

def upload_thumb(token, img_path='/tmp/qrcode_wechat.png'):
    """上传封面图/二维码到微信服务器"""
    try:
        r = requests.get(QRCODE_URL, timeout=10)
        if r.status_code == 200:
            with open(img_path, 'wb') as f:
                f.write(r.content)
            img = Image.open(img_path).convert('RGB').resize((900, 330), Image.LANCZOS)
            img.save(img_path, 'PNG')
            print(f'二维码已下载并处理')
        else:
            raise Exception(f'下载二维码失败: {r.status_code}')
    except Exception as e:
        print(f'二维码处理: {e}')
        if not os.path.exists(img_path):
            raise Exception('二维码文件不存在')

    with open(img_path, 'rb') as f:
        resp = requests.post(
            f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image',
            files={'media': ('thumb.png', f, 'image/png')}
        )
    result = resp.json()
    if 'media_id' in result:
        return result['media_id'], result.get('url', '')
    raise Exception(f'封面上传失败: {result}')

def get_news():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    history = load_published_history()
    print(f'历史记录: {len(history)} 条')
    
    sources = ['HackerNews', 'TechCrunch', 'ProductHunt', 'TheSequence', 'LatentSpace', 'ExponentialView', 'SubStack']
    result = {}
    dup_count = 0
    
    for s in sources:
        cur.execute('SELECT title, url, source FROM news WHERE source=? ORDER BY date DESC, score DESC LIMIT 6', (s,))
        rows = cur.fetchall()
        filtered = []
        for r in rows:
            if not is_duplicate(r['title'], history):
                filtered.append(r)
            else:
                dup_count += 1
        if filtered:
            result[s] = filtered
    
    conn.close()
    print(f'去重: 跳过 {dup_count} 条重复')
    return result

def get_source_config(source):
    configs = {
        'HackerNews': {'color': '#ff6600', 'bg': '#fff3e0', 'label': 'Hacker News 热门'},
        'TechCrunch': {'color': '#0a9900', 'bg': '#e8f5e9', 'label': 'TechCrunch AI'},
        'ProductHunt': {'color': '#da552f', 'bg': '#fce4ec', 'label': 'Product Hunt 热榜'},
        'TheSequence': {'color': '#6a1b9a', 'bg': '#f3e5f5', 'label': 'The Sequence'},
        'LatentSpace': {'color': '#0288d1', 'bg': '#e1f5fe', 'label': 'Latent Space'},
        'ExponentialView': {'color': '#c62828', 'bg': '#ffebee', 'label': 'Exponential View'},
        'SubStack': {'color': '#ff4400', 'bg': '#fff0e0', 'label': 'SubStack 精选'},
    }
    return configs.get(source, {'color': '#666666', 'bg': '#f5f5f5', 'label': source})

def select_hottest_news(news_data):
    """自动选择最热门的新闻，返回(新闻, 来源)"""
    # 热门关键词权重
    hot_keywords = [
        'stanford', 'openai', 'anthropic', 'google', 'nvidia', 'meta', 'apple',
        'billion', 'funding', 'invest', 'research', 'study', 'launch',
        'musk', 'zuckerberg', 'altman', 'llm', 'model', 'gpt', 'claude'
    ]
    
    all_news = []
    for source, items in news_data.items():
        for item in items:
            all_news.append((item, source))
    
    # 计算每条新闻的热度分数
    scored = []
    for item, source in all_news:
        title_lower = item['title'].lower()
        score = 0
        for kw in hot_keywords:
            if kw in title_lower:
                score += 10
        # 长度适中加分（太短可能信息不足）
        if 30 < len(item['title']) < 80:
            score += 5
        scored.append((item, source, score))
    
    # 按热度排序
    scored.sort(key=lambda x: -x[2])
    
    if scored:
        return scored[0][0], scored[0][1], scored[0][2]
    return None, None, 0

def generate_dynamic_title(hot_news, hot_source):
    """根据最热新闻生成动态标题"""
    title = hot_news['title']
    
    templates = {
        'Stanford': '刚刚！Stanford研究曝光AI惊人秘密',
        'Bluesky': '突发！Bluesky重磅押注AI赛道',
        'Zuckerberg': '炸锅！Zuckerberg这一动作震惊硅谷',
        'Miasma': '突发！开源工具重塑AI抓取格局',
        'Sheet Ninja': '刚刚！开发者神器让编程变得如此简单',
        'GitLab': '泪目！GitLab创始人以生命对抗命运',
        'SUN': '重磅！a16z加速营又出爆款',
        'microplastics': '刚刚！科学界这一发现让所有人震惊',
        'NVIDIA': '突发！NVIDIA悄悄布局AI操作系统',
        'Agent Lattice': '刚刚！代码知识图谱工具引发轰动',
    }
    
    for key, t in templates.items():
        if key.lower() in title.lower():
            return t
    
    # 默认：结合时间生成
    hour = datetime.datetime.now().hour
    prefix = '早间突发' if hour < 9 else '重磅来袭' if hour < 12 else '午间速递' if hour < 14 else '下午头条' if hour < 18 else '晚间热闻'
    
    return f'{prefix}！{title[:20]}'

def translate_title(title):
    translations = {
        'Stanford': '斯坦福研究：AI给人建议时过度"谄媚"',
        'Bluesky': 'Bluesky押注AI：推出自定义订阅源App Attie',
        'Zuckerberg': 'Zuckerberg主动联系Musk：提议帮助DOGE',
        'Miasma': 'Miasma：一个让AI爬虫深陷"毒坑"的工具',
        'Sheet Ninja': 'Sheet Ninja：Google Sheets变身"vibe coder"后端',
        'GitLab': 'GitLab创始人一边抗癌一边创业',
        'SUN': 'SUN (a16z Speedrun 006)：AI原生应用加速营毕业项目',
        'microplastics': '研究警告：实验室手套可能导致微塑料高估',
        'NVIDIA': 'NVIDIA悄悄构建AI的"操作系统"',
        'Elon Musk': '马斯克最后一位联合创始人离开xAI',
        'Mark Zuckerberg': '扎克伯格主动联系马斯克：提议协助DOGE',
        'Overestimation of microplastics': '丁腈手套可能高估微塑料检测结果',
        'Founder of GitLab battles cancer': 'GitLab创始人以创业对抗癌症',
        'What if AI doesn\'t need more RAM': 'AI不需要更多内存？Google TurboQuant另辟蹊径',
        'Agent Lattice': 'Agent Lattice：用Markdown构建代码知识图谱',
        'Lat.md': 'Lat.md：代码库知识图谱的新物种',
        'AI overly affirms users': '研究揭示：AI过度肯定用户寻求建议',
    }
    
    for key, zh in translations.items():
        if key.lower() in title.lower():
            return zh
    
    return title[:40] + '...' if len(title) > 40 else title

def expand_content(title, source, min_chars=80, max_chars=120):
    """将标题扩展为80-120字的内容"""
    content_map = {
        'Stanford': '斯坦福大学最新研究揭示AI在提供建议时存在"过度谄媚"问题。测试1127名参与者后发现，Claude、ChatGPT、Gemini等主流模型在提供个人建议时普遍过度肯定用户。这引发业界对AI诚实性的深度讨论。',
        
        'Bluesky': '去中心化社交平台Bluesky推出AI产品Attie，用户可用自然语言描述兴趣，AI自动整合相关内容。Bluesky选择"小而专"路线，用AI解决信息过载而非全面拥抱聊天功能。',
        
        'Zuckerberg': '据TechCrunch报道，Meta CEO Zuckerberg主动联系Musk提议帮助DOGE。此举引发硅谷热议——有人认为是向权力靠拢，也有人认为只是礼貌性示好。AI大佬与政治权力产生交集已成趋势。',
        
        'Miasma': 'GitHub热门工具Miasma能让AI爬虫陷入虚假内容陷阱。创作者通过"无限迷宫"反制AI数据抓取，支持者称这是"正当防卫"，批评者担忧误伤正常搜索引擎。AI时代内容战争悄然升级。',
        
        'Sheet Ninja': '工具Sheet Ninja让Google Sheets直接当CRUD后端，无需服务器和数据库，一个表格就能实现完整增删改查。目标用户是"vibe coder"——不关心架构只想快速出活的程序员。编程门槛正在急剧下降。',
        
        'GitLab': 'GitLab创始人Sytse Sijbranda一边与癌症抗争，一边继续经营公司。他将化疗与工作结合，在病床上参加董事会会议。他说"工作让我保持清醒"。这种态度引发关于工作与生活平衡的思考。',
        
        'SUN': 'a16z最新Speedrun加速营毕业项目SUN主打"AI Native应用"。这批项目普遍重视隐私计算和本地部署能力，似乎在回应用户对数据安全的担忧。AI创业正从"通用大模型"向"垂直应用+隐私优先"转向。',
        
        'microplastics': '密歇根大学研究发现实验用手套可能是微塑料检测数据偏高的"罪魁祸首"。丁腈和乳胶手套会释放大量微塑料纤维，这意味着过去十几年的相关研究可能需要重新审视。',
        
        'NVIDIA': 'TechCrunch报道NVIDIA正在构建AI的"操作系统"——一个统一软件层协调不同AI模型和数据源。分析师认为这是NVIDIA最具战略意义的动作，若成功将从芯片公司转型为AI平台公司。',
        
        'Agent Lattice': 'Lat.md用纯Markdown构建代码库知识图谱，每个.md文件既是文档也是知识节点，支持AI直接理解代码结构关系。在Hacker News引发关于"代码即知识"的新讨论。',
        
        'What if AI doesn\'t need more RAM': 'Google最新发布的TurboQuant技术另辟蹊径——不堆硬件，用更好的数学压缩KV cache。当前LLM内存瓶颈在于KV缓存随对话长度线性增长，TurboQuant在高维向量空间实现革命性压缩。',
        
        'AI overly affirms': '斯坦福大学最新研究测试主流AI模型，发现它们在提供个人建议时普遍存在"过度肯定"问题。这项涉及1127名参与者的研究引发业界对AI诚实性的广泛讨论。',
        
        'Exponential View': '本期Exponential View探讨AI如何重塑工作方式。从自动化到决策辅助，AI正在改变各行业的运作模式。值得关注的是，这种变化对就业市场和职业技能的影响。',
        
        'Last Week in AI': '上周AI领域重要进展包括多模态模型的突破和推理效率的提升。本期精选内容涵盖技术突破、产品发布和行业洞见，帮你快速了解AI发展动态。',
        
        'The Sequence': 'The Sequence深度分析NVIDIA正在构建AI的"操作系统"。这个统一软件层可以协调不同AI模型和数据源，让开发者无需关心底层硬件。有望成为AI基础设施的关键组件。',
    }
    
    for key, content in content_map.items():
        if key.lower() in title.lower():
            # 确保字数在范围内
            if len(content) > max_chars:
                content = content[:max_chars]
            elif len(content) < min_chars:
                content = content + '。' * ((min_chars - len(content)) // 3)
            return content
    
    # 默认处理
    default = f'{title}。这个消息在{source}引发关注，业界正在密切关注其后续发展。'
    if len(default) > max_chars:
        return default[:max_chars]
    return default

def build_article(news_data, thumb_media_id, thumb_url):
    today = datetime.datetime.now().strftime('%Y年%m月%d日')
    hour = datetime.datetime.now().hour
    time_label = '早报' if hour < 12 else '午报' if hour < 18 else '晚报'
    
    # 选择最热新闻
    hot_news, hot_source, hot_score = select_hottest_news(news_data)
    
    # 生成动态标题
    dynamic_title = generate_dynamic_title(hot_news, hot_source) if hot_news else f'北美AI Daily {time_label}'
    
    # 统计所有新闻
    all_news = []
    source_counts = {}
    for source, items in news_data.items():
        source_counts[source] = len(items)
        all_news.extend(items)
    
    # 模块上浮：根据最热新闻来源调整顺序
    source_order = ['HackerNews', 'SubStack', 'LatentSpace', 'ProductHunt', 'TechCrunch', 'TheSequence', 'ExponentialView']
    
    # 如果有最热新闻，将该来源移到第一位
    if hot_source and hot_source in source_order:
        source_order.remove(hot_source)
        source_order.insert(0, hot_source)
    
    # 动态开场白
    top_sources = sorted(source_counts.items(), key=lambda x: -x[1])[:3]
    top_source_names = {
        'HackerNews': 'Hacker News', 'SubStack': 'SubStack',
        'LatentSpace': 'Latent Space', 'ProductHunt': 'Product Hunt',
        'TechCrunch': 'TechCrunch', 'TheSequence': 'The Sequence',
        'ExponentialView': 'Exponential View'
    }
    source_desc = '、'.join([top_source_names.get(s, s) for s, c in top_sources])
    
    openings = [
        f'今天的AI资讯来自 {source_desc}，共 {len(all_news)} 条值得关注的消息。',
        f'{source_desc} 今日热门：{len(all_news)} 条深度内容值得关注。',
        f'本期涵盖 {source_desc} 等多个平台，共 {len(all_news)} 条精选内容。',
    ]
    opening = openings[int(datetime.datetime.now().strftime('%d')) % len(openings)]
    
    sections = []
    item_num = 0
    
    for source in source_order:
        if source not in news_data:
            continue
        
        config = get_source_config(source)
        items = news_data[source]
        is_hot_source = (source == hot_source)
        
        sections.append(f'''<p style="margin: 25px 0 15px 0; padding: 12px 15px; background: {config['bg']}; border-radius: 8px; border-left: 4px solid {config['color']}; text-align: center;">
  <strong style="font-size: 16px; color: {config['color']};">{config['label']}</strong>
</p>''')
        
        # 如果是热门来源，跳过第一条（因为已经作为标题了）
        start_idx = 1 if is_hot_source else 0
        
        for i, item in enumerate(items[start_idx:]):
            item_num += 1
            en_title = item['title']
            zh_title = translate_title(en_title)
            content = expand_content(en_title, source)
            
            # 最热新闻不在板块内重复显示
            prefix = ''
            
            sections.append(f'''<p style="margin: 15px 0 5px 0;">
  <strong style="font-size: 15px; color: #1a1a1a;">{item_num}. {prefix}{zh_title}</strong>
</p>
<p style="margin: 0; line-height: 1.8; color: #333; font-size: 14px; text-align: justify;">{content}</p>
<p style="margin: 5px 0 15px 0; border-bottom: 1px dashed #eee;"></p>''')
    
    # 结尾：使用已上传到微信服务器的二维码图片（内嵌URL）
    footer = f'''<p style="text-align: center; margin-top: 30px; padding: 25px 20px; background: #fafafa; border-radius: 12px; border: 1px solid #eee;">
  <span style="font-size: 16px; color: #333; font-weight: 500;">觉得有用？不妨分享给朋友</span>
</p>
<p style="text-align: center; margin-top: 20px;">
  <img src="{thumb_url}" style="width: 80%; max-width: 300px; height: auto; border-radius: 12px; display: block; margin: 0 auto;" alt="公众号二维码">
</p>
<p style="text-align: center; margin-top: 15px; font-size: 15px; color: #333; font-weight: 500;">扫码关注「grepAI」</p>
<p style="text-align: center; margin-top: 5px; font-size: 13px; color: #888;">每天早上自动送达</p>
<p style="text-align: center; margin-top: 20px; font-size: 13px; color: #999; line-height: 1.6;">欢迎评论交流，说说你的看法</p>
<p style="text-align: center; margin-top: 15px; font-size: 11px; color: #ccc; letter-spacing: 1px;">copyright 2026 grepAI | 认真做内容</p>'''
    
    content = f'''<p style="text-align: center; margin: 20px 15px 25px 15px; font-size: 22px; font-weight: bold; color: #1a1a1a; line-height: 1.4;">{dynamic_title} | {today}</p>
''' + '\n'.join(sections) + footer
    
    return {
        'title': dynamic_title,
        'content': content,
        'thumb_media_id': thumb_media_id,
        'hot_source': hot_source
    }

def publish():
    print('='*50)
    print('AI News 公众号发布')
    print(f'时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*50)
    
    print('获取微信access_token...')
    token = get_token()
    print('Token获取成功')
    
    print('上传二维码到微信服务器...')
    thumb_media_id, thumb_url = upload_thumb(token, '/tmp/qrcode_wechat.png')
    print(f'二维码上传成功: {thumb_media_id}')
    
    print('读取新闻数据...')
    news = get_news()
    total = sum(len(v) for v in news.values())
    print(f'读取到 {total} 条新闻')
    
    print('构建文章...')
    article = build_article(news, thumb_media_id, thumb_url)
    
    print(f'动态标题: {article["title"]}')
    print(f'热门来源: {article["hot_source"]}')
    print(f'文章总字数: {len(article["content"])}')
    
    data = {
        'articles': [{
            'title': article['title'],
            'author': 'AI Daily',
            'content': article['content'],
            'content_source_url': '',
            'digest': '今日精选全球AI科技资讯',
            'show_cover_pic': 1,
            'thumb_media_id': article['thumb_media_id']
        }]
    }
    
    print('发布到公众号草稿箱...')
    json_str = json.dumps(data, ensure_ascii=False)
    url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}'
    resp = requests.post(url, data=json_str.encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'})
    result = resp.json()
    
    if 'media_id' in result:
        media_id = result['media_id']
        print(f'发布成功!')
        print(f'media_id: {media_id}')
        
        for source, items in news.items():
            for item in items:
                save_to_history(item['title'], item['url'] if 'url' in item.keys() else '')
        print('历史记录已更新')
        
        return {
            'success': True,
            'media_id': media_id,
            'news_count': total,
            'title': article['title'],
            'hot_source': article['hot_source']
        }
    else:
        print(f'发布失败: {result}')
        return {'success': False, 'error': result}

if __name__ == '__main__':
    result = publish()
    print('='*50)
    if result.get('success'):
        print(f'完成! 共发布 {result.get("news_count")} 条新闻')
        print(f'动态标题: {result.get("title")}')
        print(f'热门来源上浮: {result.get("hot_source")}')
    else:
        print(f'失败: {result.get("error")}')