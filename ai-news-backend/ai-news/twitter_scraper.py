"""
Twitter/X Scraper for Railway deployment
Lightweight version using requests + BeautifulSoup
For heavy-duty scraping, use twitter_scraper_playwright.py
"""

import os
import re
import json
import asyncio
import requests
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

# Twitter accounts to monitor for AI news
TWITTER_ACCOUNTS = [
    "ErnestoSoftware",
    "sama",           # Sam Altman
    "elonmusk",       # Elon Musk
    "AndrewYNg",      # Andrew Ng
    "ylecun",         # Yann LeCun
    "JeffDean",       # Jeff Dean
    "GaryMarcus",     # Gary Marcus
    "AnthropicAI",    # Anthropic
    "GoogleAI",       # Google AI
    "MetaAI",         # Meta AI
    "xAI",            # xAI
    "MikeKrieger",    # Mike Krieger
    "nvidia",         # NVIDIA
    "SatyaNadella",   # Satya Nadella
    "sundarpichai",   # Sundar Pichai
]

SEARCH_QUERIES = [
    "AI OR artificial intelligence OR GPT",
    "OpenAI OR Anthropic OR Claude",
    "machine learning OR LLM",
]


class TwitterScraper:
    """Lightweight Twitter scraper using requests"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
    
    def get_tweets_via_nitter(self, username: str, limit: int = 10) -> List[Dict]:
        """Get tweets using Nitter instances (free, no auth needed)"""
        tweets = []
        
        # Try multiple Nitter instances
        nitter_instances = [
            "nitter.privacydev.net",
            "nitter.poast.org", 
            "nitter.net",
            "nitter.unixfox.eu",
        ]
        
        for instance in nitter_instances:
            try:
                url = f"https://{instance}/{username}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find tweet containers
                    tweet_divs = soup.find_all('div', class_='tweet-content')
                    
                    for div in tweet_divs[:limit]:
                        text = div.get_text(strip=True)
                        if text:
                            tweets.append({
                                'username': username,
                                'text': text,
                                'source': f'nitter ({instance})'
                            })
                    
                    if tweets:
                        print(f"  ✓ Got {len(tweets)} tweets from @{username} via {instance}")
                        break
                        
            except Exception as e:
                continue
        
        if not tweets:
            print(f"  ✗ Could not fetch @{username} from any Nitter instance")
        
        return tweets
    
    def get_tweets_via_fxtwitter(self, username: str, limit: int = 10) -> List[Dict]:
        """Get tweets using fxtwitter (vxtwitter) API - FREE and works!"""
        tweets = []
        
        try:
            # Use the fxtwitter API (free, no auth)
            url = f"https://api.fxtwitter.com/v1/user/by/tweet/{username}?include_replies=false&limit={limit}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check the API response structure
                if 'tweet' in data:
                    tweet_data = data['tweet']
                    if 'media' in tweet_data and 'tweets' in tweet_data['media']:
                        for tweet in tweet_data['media']['tweets']:
                            tweets.append({
                                'username': username,
                                'text': tweet.get('text', ''),
                                'time': tweet.get('created_at', ''),
                                'metrics': tweet.get('metrics', {}),
                                'url': tweet.get('url', ''),
                                'source': 'fxtwitter API'
                            })
                elif 'legacy' in data:
                    # Another response format
                    legacy = data.get('legacy', {})
                    for tweet in legacy.get('tweets', [])[:limit]:
                        tweets.append({
                            'username': username,
                            'text': tweet.get('text', ''),
                            'time': tweet.get('created_at', ''),
                            'source': 'fxtwitter API'
                        })
                
                if tweets:
                    print(f"  ✓ Got {len(tweets)} tweets from @{username} via fxtwitter")
                    return tweets
                    
        except Exception as e:
            print(f"  fxtwitter error for @{username}: {e}")
        
        return tweets
    
    def get_tweets_via_tweeterid(self, username: str, limit: int = 10) -> List[Dict]:
        """Alternative method using tweeterid or other free APIs"""
        tweets = []
        
        # Try vxtwitter.com (redirect method)
        try:
            url = f"https://vxtwitter.com/{username}"
            response = self.session.get(url, timeout=10, allow_redirects=False)
            
            # This might redirect to the tweet, but let's try another approach
        except Exception as e:
            pass
        
        return tweets


async def fetch_twitter_ai_news_async(accounts: List[str] = None, queries: List[str] = None) -> Dict:
    """
    Main async function to fetch AI-related tweets
    """
    if accounts is None:
        accounts = TWITTER_ACCOUNTS
    
    all_tweets = {
        "accounts": [],
        "timestamp": datetime.now().isoformat(),
        "source": "fxtwitter + nitter"
    }
    
    scraper = TwitterScraper()
    
    print("Fetching tweets from accounts...")
    
    # Try fxtwitter API first (most reliable)
    for username in accounts:
        print(f"  Fetching @{username}...")
        
        # Try fxtwitter first
        tweets = scraper.get_tweets_via_fxtwitter(username)
        
        # If that fails, try Nitter
        if not tweets:
            tweets = scraper.get_tweets_via_nitter(username)
        
        if tweets:
            all_tweets["accounts"].extend(tweets)
    
    return all_tweets


def fetch_twitter_ai_news(accounts: List[str] = None, queries: List[str] = None) -> Dict:
    """
    Main sync function to fetch AI-related tweets
    """
    return asyncio.run(fetch_twitter_ai_news_async(accounts, queries))


def save_tweets_to_json(tweets: Dict, filename: str = None):
    """Save tweets to JSON file"""
    if filename is None:
        filename = f"twitter_ai_{datetime.now().strftime('%Y%m%d')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {filename}")


# Test
if __name__ == "__main__":
    tweets = fetch_twitter_ai_news()
    print(f"\nTotal tweets fetched: {len(tweets.get('accounts', []))}")
    print(json.dumps(tweets, ensure_ascii=False, indent=2))
    save_tweets_to_json(tweets)
