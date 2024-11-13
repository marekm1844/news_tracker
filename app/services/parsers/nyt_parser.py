from bs4 import BeautifulSoup
from .base_parser import BaseParser
from typing import Dict
import requests
from urllib.parse import urlparse
import httpx
import newspaper

class NYTParser(BaseParser):
    async def parse(self, url: str) -> Dict[str, str]:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            }
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = "https://" + url
             
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
            
            if response.status_code != 200:
                raise httpx.HTTPStatusError(f'Failed to fetch article: HTTP {response.status_code}', request=response.request, response=response)
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get the article title from newspaper
            article = newspaper.Article(url)
            article.download(input_html=response.text)
            article.parse()
            title = article.title
            
            # Find the main article content
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