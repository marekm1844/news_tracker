from newspaper import Article as NewsArticle
from typing import Dict
from .base_parser import BaseParser

class GenericParser(BaseParser):
    def parse(self, url: str) -> Dict[str, str]:
        news_article = NewsArticle(url)
        news_article.download()
        news_article.parse()

        return {
            'title': news_article.title,
            'content': news_article.text
        }