from abc import ABC, abstractmethod
from typing import Dict

class BaseParser(ABC):
    @abstractmethod
    async def parse(self, url: str) -> Dict[str, str]:
        """
        Asynchronously parse the article from the given URL.

        Returns:
            A dictionary with keys 'title' and 'content'.
        """
        pass