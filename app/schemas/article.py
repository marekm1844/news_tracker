from pydantic import BaseModel, Field
from datetime import datetime

class ArticleBase(BaseModel):
    url: str = Field(
        ...,
        description="The URL of the article to track",
        example="https://www.nytimes.com/2024/11/12/world/middleeast/israel-north-gaza-hamas-war.html"
    )

class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int = Field(..., description="Unique identifier for the article")
    title: str = Field(..., description="The title of the article")
    content: str = Field(..., description="The full content of the article")
    created_at: datetime = Field(..., description="When the article was first tracked")

    class Config:
        from_attributes = True