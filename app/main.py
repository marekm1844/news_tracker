from fastapi import FastAPI
from .routers import articles
from .database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="News Tracker API",
    description="API to track changes in online news articles over time.",
    version="0.1.0",
)

app.include_router(articles.router)