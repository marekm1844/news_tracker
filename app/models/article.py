from sqlalchemy import Column, Integer, String, Text, DateTime, func
from ..database import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())