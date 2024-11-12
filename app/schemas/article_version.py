# app/schemas/article_version.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class ArticleVersionBase(BaseModel):
    title: str
    content: str
    created_at: datetime

class ArticleVersionResponse(ArticleVersionBase):
    id: int
    diff: Optional[str] = None

    class Config:
        from_attributes = True