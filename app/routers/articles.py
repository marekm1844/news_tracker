from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.article import ArticleCreate, ArticleResponse
from ..services.article_service import ArticleService
from ..dependencies import get_db
from typing import List

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = ArticleService.create_article(db, article)
    return db_article

@router.get("/", response_model=List[ArticleResponse])
def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = ArticleService.get_articles(db, skip=skip, limit=limit)
    return articles

@router.get("/{article_id}", response_model=ArticleResponse)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = ArticleService.get_article(db, article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article