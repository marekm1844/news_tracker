from abc import ABC, abstractmethod
from typing import Dict
import aiohttp
from bs4 import BeautifulSoup

class ParserError(Exception):
    """Custom exception for parser-related errors"""
    pass

class BaseParser(ABC):
    @abstractmethod
    async def parse(self, url: str) -> Dict[str, str]:
        """
        Asynchronously parse the article from the given URL.

        Returns:
            A dictionary with keys 'title' and 'content'.
        """
        pass

    async def _fetch_and_parse(self, url: str) -> 'BeautifulSoup':
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise ParserError(f"Failed to fetch URL: {url}. Status: {response.status}")
                    html = await response.text()
                    return BeautifulSoup(html, 'html.parser')
        except Exception as e:
            raise ParserError(f"Error fetching or parsing URL: {str(e)}")