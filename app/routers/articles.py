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
async def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article_version = await ArticleService.create_or_update_article(db, article)
    return db_article_version

@router.get("/", response_model=List[ArticleResponse])
async def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = await ArticleService.get_articles(db, skip=skip, limit=limit)
    return articles

@router.get("/{article_id}", response_model=ArticleResponse)
async def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = await ArticleService.get_article(db, article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.get("/{article_id}/versions", response_model=List[ArticleVersionResponse])
async def read_article_versions(article_id: int, db: Session = Depends(get_db)):
    versions = await ArticleService.get_article_versions(db, article_id)
    if not versions:
        raise HTTPException(status_code=404, detail="No versions found for this article")
    return versions

@router.get("/{article_id}/versions/{version_id}/diff", response_model=str)
async def read_version_diff(article_id: int, version_id: int, db: Session = Depends(get_db)):
    result = await db.execute(select(ArticleVersion).where(
        ArticleVersion.id == version_id,
        ArticleVersion.article_id == article_id
    ))
    version = result.scalars().first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    return version.diff