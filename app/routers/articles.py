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
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)

@router.post("/", 
    response_model=ArticleVersionResponse,
    summary="Create a new article",
    description="""
    Create a new article to track by providing its URL.
    
    The API will:
    * Fetch the article content
    * Store it in the database
    * Begin tracking it for changes
    
    If the article already exists, it will check for updates and create a new version if changes are detected.
    """,
    response_description="The created or updated article version"
)
async def create_article(
    article: ArticleCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new article or update an existing one.
    """
    db_article_version = await ArticleService.create_or_update_article(db, article)
    return db_article_version

@router.get("/", 
    response_model=List[ArticleResponse],
    summary="List all articles",
    description="Retrieve a paginated list of all tracked articles.",
    response_description="List of articles"
)
async def read_articles(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """
    Get all articles with pagination support.
    """
    articles = await ArticleService.get_articles(db, skip=skip, limit=limit)
    return articles

@router.get("/{article_id}", 
    response_model=ArticleResponse,
    summary="Get article by ID",
    description="Retrieve a specific article by its ID.",
    response_description="The requested article",
    responses={
        404: {
            "description": "Article not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Article not found"}
                }
            }
        }
    }
)
async def read_article(
    article_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get a specific article by ID.
    """
    db_article = await ArticleService.get_article(db, article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.get("/{article_id}/versions", 
    response_model=List[ArticleVersionResponse],
    summary="Get article versions",
    description="""
    Retrieve all versions of a specific article.
    
    This endpoint returns the version history of an article, showing how it has changed over time.
    Versions are ordered from newest to oldest.
    """,
    response_description="List of article versions",
    responses={
        404: {
            "description": "No versions found",
            "content": {
                "application/json": {
                    "example": {"detail": "No versions found for this article"}
                }
            }
        }
    }
)
async def read_article_versions(
    article_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get all versions of a specific article.
    """
    versions = await ArticleService.get_article_versions(db, article_id)
    if not versions:
        raise HTTPException(status_code=404, detail="No versions found for this article")
    return versions

@router.get("/{article_id}/versions/{version_id}/diff", 
    response_model=str,
    summary="Get version diff",
    description="""
    Retrieve the HTML diff between this version and the previous version.
    
    The diff shows:
    * Added content in green
    * Removed content in red
    * Unchanged content in black
    """,
    response_description="HTML formatted diff",
    responses={
        404: {
            "description": "Version not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Version not found"}
                }
            }
        }
    }
)
async def read_version_diff(
    article_id: int, 
    version_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get the diff for a specific version of an article.
    """
    result = await db.execute(select(ArticleVersion).where(
        ArticleVersion.id == version_id,
        ArticleVersion.article_id == article_id
    ))
    version = result.scalars().first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    return version.diff