# app/services/article_service.py

from sqlalchemy.orm import Session
from ..models.article import Article
from ..models.article_version import ArticleVersion
from ..schemas.article import ArticleCreate
from .parsers.parser_factory import ParserFactory
from ..utils.diff_utils import compare_versions

class ArticleService:
    @staticmethod
    def create_or_update_article(db: Session, article_create: ArticleCreate):
        parser = ParserFactory.get_parser(article_create.url)
        try:
            parsed_data = parser.parse(article_create.url)
        except Exception as e:
            raise Exception(f"Failed to parse article: {str(e)}")

        # Check if article exists
        db_article = db.query(Article).filter(Article.url == article_create.url).first()
        if not db_article:
            # Create new article
            db_article = Article(url=article_create.url)
            db.add(db_article)
            db.commit()
            db.refresh(db_article)

        # Get the latest version
        latest_version = db.query(ArticleVersion).filter(
            ArticleVersion.article_id == db_article.id
        ).order_by(ArticleVersion.created_at.desc()).first()

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
            db.commit()
            db.refresh(new_version)
            return new_version  # Return the new version
        else:
            # No content change, return the latest version
            return latest_version

    @staticmethod
    def get_article_versions(db: Session, article_id: int):
        return db.query(ArticleVersion).filter(
            ArticleVersion.article_id == article_id
        ).order_by(ArticleVersion.created_at.desc()).all()