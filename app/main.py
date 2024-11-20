from fastapi import FastAPI
import uvicorn
from .routers import articles
from .database import engine, Base
import asyncio
from .scheduler import start_scheduler
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="News Tracker API",
    description="""
    News Tracker API allows you to monitor changes in online news articles over time.
    
    ## Features
    * Track articles from various news sources
    * Automatically detect and store article changes
    * View article version history
    * Compare different versions of articles
    
    ## Authentication
    Currently, the API does not require authentication.
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    logger.info("Application starting up...")
    # Any other startup logic you need (not related to DB creation)

@app.on_event("shutdown")
async def shutdown():
    logger.info("Application shutting down...")
    # Any cleanup logic you need

app.include_router(articles.router)
scheduler = start_scheduler()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )