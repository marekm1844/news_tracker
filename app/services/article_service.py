from sqlalchemy.orm import Session
from ..models.article import Article
from ..schemas.article import ArticleCreate
from newspaper import Article as NewsArticle

class ArticleService:
    @staticmethod
    def create_article(db: Session, article_create: ArticleCreate):
        # Fetch article content using Newspaper3k
        news_article = NewsArticle(article_create.url)
        news_article.download()
        news_article.parse()

        db_article = Article(
            url=article_create.url,
            title=news_article.title,
            content=news_article.text
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article

    @staticmethod
    def get_article(db: Session, article_id: int):
        return db.query(Article).filter(Article.id == article_id).first()

    @staticmethod
    def get_articles(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Article).offset(skip).limit(limit).all()