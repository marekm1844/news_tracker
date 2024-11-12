from pydantic import BaseModel
from datetime import datetime

class ArticleBase(BaseModel):
    url: str

class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True