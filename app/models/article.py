from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)

    # Relationship to versions
    versions = relationship("ArticleVersion", back_populates="article")