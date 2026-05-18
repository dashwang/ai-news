#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json

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

# 原始英文标题（从HackerNews获取）
raw_news = [
    {"title": "The Claude Code Source Leak: fake tools, frustration regexes, undercover mode", "url": "https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/", "source": "HackerNews"},
    {"title": "TinyLoRA – Learning to Reason in 13 Parameters", "url": "https://arxiv.org/abs/2602.04118", "source": "HackerNews"},
    {"title": "Ministack (Replacement for LocalStack)", "url": "https://ministack.org/", "source": "HackerNews"},
    {"title": "A dot a day keeps the clutter away", "url": "https://scottlawsonbc.com/post/dot-system", "source": "HackerNews"},
    {"title": "OpenAI closes funding round at an $852B valuation", "url": "https://www.cnbc.com/2026/03/31/openai-funding-round-ipo.html", "source": "HackerNews"},
    {"title": "TruffleRuby", "url": "https://chrisseaton.com/truffleruby/", "source": "HackerNews"},
    {"title": "Show HN: 1-Bit Bonsai, the First Commercially Viable 1-Bit LLMs", "url": "https://prismml.com/", "source": "HackerNews"},
    {"title": "4D Doom", "url": "https://github.com/danieldugas/HYPERHELL", "source": "HackerNews"},
    {"title": "Slop is not necessarily the future", "url": "https://www.greptile.com/blog/ai-slopware-future", "source": "HackerNews"},
    {"title": "Learn Something Old Every Day, Part XVIII: How Does FPU Detection Work?", "url": "https://www.os2museum.com/wp/learn-something-old-every-day-part-xviii-how-does-fpu-detection-work/", "source": "HackerNews"},
    {"title": "Open source CAD in the browser (Solvespace)", "url": "https://solvespace.com/webver.pl", "source": "HackerNews"},
    {"title": "OkCupid gave 3M dating-app photos to facial recognition firm, FTC says", "url": "https://arstechnica.com/tech-policy/2026/03/okcupid-match-pay-no-fine-for-sharing-user-photos-with-facial-recognition-firm/", "source": "HackerNews"},
]

# 中文翻译（由AI模型完成）
translated_news = [
    {"title": "Claude Code 源代码泄露：假工具、令人沮丧的正则表达式、潜伏模式", "title_cn": "Claude Code 源代码泄露事件", "url": "https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/", "source": "HackerNews"},
    {"title": "TinyLoRA – 用13个参数学会推理", "title_cn": "TinyLoRA: 13参数推理模型", "url": "https://arxiv.org/abs/2602.04118", "source": "HackerNews"},
    {"title": "Ministack (LocalStack的替代品)", "title_cn": "Ministack: LocalStack替代方案", "url": "https://ministack.org/", "source": "HackerNews"},
    {"title": "每天一个点，让杂乱远离", "title_cn": "每日一点: 整理收纳系统", "url": "https://scottlawsonbc.com/post/dot-system", "source": "HackerNews"},
    {"title": "OpenAI 以8520亿美元估值完成融资轮", "title_cn": "OpenAI 8520亿估值融资", "url": "https://www.cnbc.com/2026/03/31/openai-funding-round-ipo.html", "source": "HackerNews"},
    {"title": "TruffleRuby", "title_cn": "TruffleRuby 编译器", "url": "https://chrisseaton.com/truffleruby/", "source": "HackerNews"},
    {"title": "Show HN: 1-Bit Bonsai，首个商业可行的1位LLM", "title_cn": "1-Bit Bonsai: 首个商业1位LLM", "url": "https://prismml.com/", "source": "HackerNews"},
    {"title": "4D Doom", "title_cn": "4D版毁灭战士", "url": "https://github.com/danieldugas/HYPERHELL", "source": "HackerNews"},
    {"title": "Slop不一定是未来", "title_cn": "AI垃圾内容并非未来", "url": "https://www.greptile.com/blog/ai-slopware-future", "source": "HackerNews"},
    {"title": "每天学点旧知识，第十八部分：FPU检测是如何工作的？", "title_cn": "FPU检测原理详解", "url": "https://www.os2museum.com/wp/learn-something-old-every-day-part-xviii-how-does-fpu-detection-work/", "source": "HackerNews"},
    {"title": "浏览器中的开源CAD (Solvespace)", "title_cn": "Solvespace: 浏览器开源CAD", "url": "https://solvespace.com/webver.pl", "source": "HackerNews"},
    {"title": "OkCupid向面部识别公司提供300万约会应用照片，FTC称", "title_cn": "OkCupid泄露300万用户照片", "url": "https://arstechnica.com/tech-policy/2026/03/okcupid-match-pay-no-fine-for-sharing-user-photos-with-facial-recognition-firm/", "source": "HackerNews"},
]

def format_infoq_style(news_list):
    """格式化新闻为InfoQ风格（带颜色）"""
    output = []
    output.append(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    output.append("       🚀 全球科技要闻 Daily Tech Roundup")
    output.append(f"{'='*60}{Colors.ENDC}\n")
    
    output.append(f"\n{Colors.GREEN}{Colors.BOLD}📰 HackerNews 热门榜单{Colors.ENDC}")
    output.append(f"{Colors.GREEN}{'-'*45}{Colors.ENDC}")
    
    for i, item in enumerate(news_list[:10], 1):
        output.append(f"  {i}. {Colors.BOLD}{item['title_cn']}{Colors.ENDC}")
        output.append(f"     └─ {item['title']}")
        output.append(f"     🔗 {item['url']}")
        output.append("")
    
    output.append(f"\n{Colors.YELLOW}{Colors.BOLD}📊 统计: 共收录 {len(news_list)} 条科技资讯{Colors.ENDC}")
    output.append(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
    
    return "\n".join(output)

# 生成微信文章内容（纯文本版本）
def generate_wechat_content(news_list):
    content = []
    content.append("🚀 全球科技要闻 Daily Tech Roundup\n")
    content.append("=" * 50)
    content.append("\n📰 HackerNews 热门榜单\n")
    content.append("-" * 45)
    
    for i, item in enumerate(news_list[:10], 1):
        content.append(f"\n{i}. {item['title_cn']}")
        content.append(f"   原文: {item['title']}")
        content.append(f"   链接: {item['url']}")
    
    content.append(f"\n\n📊 统计: 共收录 {len(news_list)} 条科技资讯")
    content.append("\n" + "=" * 50)
    content.append("由 AI 自动整理 | 每天自动更新")
    
    return "\n".join(content)

if __name__ == "__main__":
    # 打印带颜色的终端输出
    print(format_infoq_style(translated_news))
    
    # 输出JSON数据（用于微信发布）
    wechat_content = generate_wechat_content(translated_news)
    
    result = {
        "content_type": "application/json; charset=utf-8",
        "content": wechat_content,
        "news_count": len(translated_news),
        "sources": ["HackerNews", "ProductHunt(需要认证)", "TechCrunch(需API)", "TheSequence(付费)"],
        "status": "success"
    }
    
    print("\n--- JSON OUTPUT FOR WECHAT ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))