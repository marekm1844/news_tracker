from bs4 import BeautifulSoup
from .base_parser import BaseParser
from typing import Dict
import requests
from urllib.parse import urlparse

class NYTParser(BaseParser):
    def parse(self, url: str) -> Dict[str, str]:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            }
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = "https://" + url
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get the article title from newspaper
            import newspaper
            article = newspaper.Article(url)
            article.download()
            article.parse()
            title = article.title
            
            # Find the main article content
            article_content = []
            # Look for paragraphs within the main article section
            content_section = soup.find('section', {'name': 'articleBody'}) or soup.find_all()
            if content_section:
                paragraphs = content_section.find_all('p')
                article_content = [p.get_text().strip() for p in paragraphs]
            
            return {
                'title': title,
                'content': '\n\n'.join(article_content)
            }
        except requests.exceptions.RequestException as e:
            return {
                'title': '',
                'content': str(e)
            }