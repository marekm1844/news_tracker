from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.article import ArticleCreate, ArticleResponse
from ..services.article_service import ArticleService
from ..dependencies import get_db
from typing import List
from ..models.article_version import ArticleVersion
from ..schemas.article_version import ArticleVersionResponse

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ArticleVersionResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article_version = ArticleService.create_or_update_article(db, article)
    return db_article_version

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

@router.get("/{article_id}/versions", response_model=List[ArticleVersionResponse])
def read_article_versions(article_id: int, db: Session = Depends(get_db)):
    versions = ArticleService.get_article_versions(db, article_id)
    if not versions:
        raise HTTPException(status_code=404, detail="No versions found for this article")
    return versions

@router.get("/{article_id}/versions/{version_id}/diff", response_model=str)
def read_version_diff(article_id: int, version_id: int, db: Session = Depends(get_db)):
    version = db.query(ArticleVersion).filter(
        ArticleVersion.id == version_id,
        ArticleVersion.article_id == article_id
    ).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    return version.diff