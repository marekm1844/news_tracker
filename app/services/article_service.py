# app/services/article_service.py

from sqlalchemy.orm import Session
from ..models.article import Article
from ..models.article_version import ArticleVersion
from ..schemas.article import ArticleCreate
from .parsers.parser_factory import ParserFactory
from ..utils.diff_utils import compare_versions
from sqlalchemy import select
from ..exeptions.parser_error import ParsingError

class ArticleService:
    @staticmethod
    def article_model():
        return Article

    @staticmethod
    def article_version_model():
        return ArticleVersion 
    @staticmethod
    async def create_or_update_article(db: Session, article_create: ArticleCreate):
        parser = ParserFactory.get_parser(article_create.url)
        try:
            parsed_data = await parser.parse(article_create.url)
        except (ValueError, ConnectionError, ParserError) as e:
            raise ParsingError(f"Failed to parse article: {str(e)}")

        # Check if article exists
        result = await db.execute(select(Article).where(Article.url == article_create.url))
        db_article = result.scalars().first()

        if not db_article:
            # Create new article
            db_article = Article(url=article_create.url)
            db.add(db_article)
            await db.commit()
            await db.refresh(db_article)

        # Get the latest version
        result = await db.execute(select(ArticleVersion).where(
            ArticleVersion.article_id == db_article.id
        ).order_by(ArticleVersion.created_at.desc()))
        latest_version = result.scalars().first()

        # Check if content has changed
        content_changed = True
        if latest_version and latest_version.content == parsed_data['content']:
            content_changed = False

        if content_changed:
            # Compute diff if not the first version
            diff_html = None
            if latest_version:
                diff_html = compare_versions(latest_version.content, parsed_data['content'])
            else:
                diff_html = None

            # Insert new version
            new_version = ArticleVersion(
                article_id=db_article.id,
                title=parsed_data['title'],
                content=parsed_data['content'],
                diff=diff_html
            )
            db.add(new_version)
            await db.commit()
            await db.refresh(new_version)
            return new_version  # Return the new version
        else:
            # No content change, return the latest version
            return latest_version

    @staticmethod
    async def get_article_versions(db: Session, article_id: int):
        result = await db.execute(select(ArticleVersion).where(
            ArticleVersion.article_id == article_id
        ).order_by(ArticleVersion.created_at.desc()))
        return result.scalars().all()
    
    @staticmethod
    async def get_article(db: Session, article_id: int):
        # Get the article version by its ID and join with the article
        result = await db.execute(
            select(Article, ArticleVersion)
            .join(ArticleVersion, Article.id == ArticleVersion.article_id)
            .where(ArticleVersion.id == article_id)
        )
        
        row = result.first()
        if not row:
            return None
            
        article, version = row
        
        # Update article attributes from the version to match schema
        article.title = version.title
        article.content = version.content
        article.created_at = version.created_at
        
        return article