#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import urllib.request
import urllib.parse
import ssl

# 确保UTF-8输出
sys.stdout.reconfigure(encoding='utf-8')

# ANSI颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def fetch_hackernews():
    """获取HackerNews热门"""
    try:
        url = "https://hackernews.api.allback.cn/v0/topstories.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            ids = json.loads(response.read().decode('utf-8'))[:10]
        
        articles = []
        for item_id in ids[:5]:
            item_url = f"https://hackernews.api.allback.cn/v0/item/{item_id}.json"
            req = urllib.request.Request(item_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                item = json.loads(response.read().decode('utf-8'))
                articles.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', f'https://news.ycombinator.com/item?id={item_id}'),
                    'source': 'HackerNews'
                })
        return articles
    except Exception as e:
        print(f"获取HackerNews失败: {e}")
        return []

def fetch_producthunt():
    """获取Product Hunt今日热门"""
    try:
        url = "https://api.producthunt.com/v2/posts"
        req = urllib.request.Request(
            url + "?sort=newest&per_page=10",
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Authorization': 'Bearer '
            }
        )
        # 使用备用API
        url = "https://www.producthunt.com/posts"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        # 简单解析（Product Hunt页面结构复杂，这里用备用方案）
        import re
        titles = re.findall(r'"name":"([^"]+)"', html)[:5]
        return [{'title': t, 'url': 'https://www.producthunt.com', 'source': 'Product Hunt'} for t in titles]
    except Exception as e:
        print(f"获取Product Hunt失败: {e}")
        return []

def fetch_techcrunch():
    """获取TechCrunch最新新闻"""
    try:
        url = "https://techcrunch.com/wp-json/tc/v1/posts?per_page=10"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        articles = []
        for post in data[:5]:
            articles.append({
                'title': post.get('title', {}).get('rendered', ''),
                'url': post.get('link', ''),
                'source': 'TechCrunch'
            })
        return articles
    except Exception as e:
        print(f"获取TechCrunch失败: {e}")
        return []

def fetch_thesequence():
    """获取TheSequence最新新闻"""
    try:
        url = "https://thesequence.substack.com"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        import re
        titles = re.findall(r'<h2[^>]*>([^<]+)</h2>', html)[:5]
        return [{'title': t.strip(), 'url': url, 'source': 'TheSequence'} for t in titles]
    except Exception as e:
        print(f"获取TheSequence失败: {e}")
        return []

# 翻译函数 - 这里用简单的模板，实际翻译由AI模型完成
def format_news(news_list):
    """格式化新闻为InfoQ风格"""
    output = []
    output.append(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    output.append("       🚀 全球科技要闻 Daily Tech Roundup")
    output.append(f"{'='*60}{Colors.ENDC}\n")
    
    # 按来源分组
    sources = {}
    for item in news_list:
        src = item['source']
        if src not in sources:
            sources[src] = []
        sources[src].append(item)
    
    # 输出每个来源
    source_colors = {
        'HackerNews': Colors.GREEN,
        'Product Hunt': Colors.CYAN,
        'TechCrunch': Colors.YELLOW,
        'TheSequence': Colors.RED,
        'InfoQ': Colors.BLUE
    }
    
    for src, items in sources.items():
        color = source_colors.get(src, Colors.ENDC)
        output.append(f"\n{color}{Colors.BOLD}📰 {src}{Colors.ENDC}")
        output.append(f"{color}{'-'*40}{Colors.ENDC}")
        for i, item in enumerate(items, 1):
            output.append(f"  {i}. {item.get('title_cn', item['title'])}")
            output.append(f"     🔗 {item['url']}")
        output.append("")
    
    return "\n".join(output)

if __name__ == "__main__":
    print("正在获取新闻...")
    
    all_news = []
    all_news.extend(fetch_hackernews())
    all_news.extend(fetch_techcrunch())
    all_news.extend(fetch_thesequence())
    
    # 由于API限制，Product Hunt需要认证，这里用备用
    print(f"共获取 {len(all_news)} 条新闻")
    
    # 输出原始英文（翻译将由AI模型完成）
    formatted = format_news(all_news)
    print(formatted)
    
    # 输出JSON格式用于后续处理
    print("\n--- JSON DATA ---")
    print(json.dumps(all_news, ensure_ascii=False, indent=2))