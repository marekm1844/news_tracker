from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base

class ArticleVersion(Base):
    __tablename__ = 'article_versions'

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'), index=True)
    title = Column(String)
    content = Column(Text)
    diff = Column(Text, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to article
    article = relationship("Article", back_populates="versions")