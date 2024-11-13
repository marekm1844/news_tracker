# app/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .services.article_service import ArticleService
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session
import os
from dotenv import load_dotenv
import asyncio
import logging
from sqlalchemy import select

logging.basicConfig(level=logging.INFO,
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                  handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)


load_dotenv()

async def check_articles():
    async with async_session() as db:
        try:
            result = await db.execute(select(ArticleService.article_model()))
            articles = result.scalars().all()

            batch_size = int(os.getenv('BATCH_SIZE', 10))
            # Divide articles into batches
            for i in range(0, len(articles), batch_size):
                batch = articles[i:i+batch_size]
                tasks = []
                for article in batch:
                    logger.info(f"Scheduling check for article with URL: {article.url}")
                    tasks.append(
                        ArticleService.create_or_update_article(db, article)
                    )
                # Run the tasks concurrently
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for result, article in zip(results, batch):
                    if isinstance(result, Exception):
                        logger.error(f"Error processing article {article.url}: {str(result)}")
                    else:
                        logger.info(f"Successfully processed article {article.url}")
                logger.info(f"Processed batch {i // batch_size + 1}")
        except Exception as e:
            logger.error(f"Error checking articles: {str(e)}", exc_info=True)

def start_scheduler():
    scheduler = AsyncIOScheduler()
    check_interval_hours = float(os.getenv('CHECK_INTERVAL_HOURS', 1))
    scheduler.add_job(check_articles, 'interval', hours=check_interval_hours)
    scheduler.start()
    logger.info("Scheduler started")
    return scheduler