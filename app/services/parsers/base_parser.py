from abc import ABC, abstractmethod
from typing import Dict

class BaseParser(ABC):
    @abstractmethod
    def parse(self, url: str) -> Dict[str, str]:
        """
        Parse the article from the given URL.

        Returns:
            A dictionary with keys 'title' and 'content'.
        """
        pass