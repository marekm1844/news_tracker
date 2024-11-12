from typing import Type
from urllib.parse import urlparse
from .base_parser import BaseParser
from .nyt_parser import NYTParser
from .generic_parser import GenericParser

class ParserFactory:
    @staticmethod
    def get_parser(url: str) -> BaseParser:
        domain = urlparse(url).netloc
        if 'nytimes.com' in domain:
            return NYTParser()
        else:
            return GenericParser()