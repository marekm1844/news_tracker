# app/schemas/article_version.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ArticleVersionBase(BaseModel):
    title: str = Field(..., description="The title of the article at this version")
    content: str = Field(..., description="The content of the article at this version")
    created_at: datetime = Field(..., description="When this version was created")

class ArticleVersionResponse(ArticleVersionBase):
    id: int = Field(..., description="Unique identifier for this version")
    diff: Optional[str] = Field(
        None, 
        description="HTML-formatted diff showing changes from previous version"
    )

    class Config:
        from_attributes = True