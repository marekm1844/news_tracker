from newspaper import Article as NewsArticle
from typing import Dict
from .base_parser import BaseParser
import asyncio

class GenericParser(BaseParser):
    async def parse(self, url: str) -> Dict[str, str]:
        loop = asyncio.get_event_loop()
        news_article = NewsArticle(url)
        await loop.run_in_executor(None, news_article.download)
        await loop.run_in_executor(None, news_article.parse)

        return {
            'title': news_article.title,
            'content': news_article.text
        }