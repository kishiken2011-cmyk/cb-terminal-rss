import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import re

def scrape_cb_terminal():
    """CB Terminalから記事情報を取得"""
    url = "https://cb-terminal.dev/ja"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching page: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    
    # topic-item- で始まるIDを持つdivを全て取得
    topic_items = soup.find_all('div', id=re.compile(r'^topic-item-'))
    
    for item in topic_items:
        # IDからトピックUUIDを抽出
        topic_id = item.get('id', '').replace('topic-item-', '')
        
        if not topic_id:
            continue
        
        # タイトルを取得
        title_elem = item.find('h3')
        title = title_elem.get_text(strip=True) if title_elem else 'No Title'
        
        # URLを構築
        article_url = f"https://cb-terminal.dev/ja/topic/{topic_id}"
        
        # 記事情報を追加
        article = {
            'title': title,
            'url': article_url,
            'description': title,
            'pubDate': datetime.now()
        }
        articles.append(article)
    
    print(f"Found {len(articles)} articles")
    return articles

def generate_rss(articles, output_file='cb_terminal.xml'):
    """RSSフィードを生成"""
    fg = FeedGenerator()
    fg.title('CB Terminal')
    fg.link(href='https://cb-terminal.dev/ja', rel='alternate')
    fg.description('CB Terminal 暗号資産ニュース')
    fg.language('ja')
    
    for article in articles:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['url'])
        fe.description(article['description'])
        fe.pubDate(article['pubDate'])
    
    # RSSファイルを生成
    fg.rss_file(output_file, pretty=True)
    print(f"RSS generated: {output_file}")

if __name__ == '__main__':
    articles = scrape_cb_terminal()
    if articles:
        generate_rss(articles)
    else:
        print("No articles found")
