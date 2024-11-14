from fastapi import FastAPI
import uvicorn
from .routers import articles
from .database import engine, Base
import asyncio
from .scheduler import start_scheduler
from fastapi.middleware.cors import CORSMiddleware
# Create all tables
# Note: For async engine, you need to use an async context


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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app.include_router(articles.router)
scheduler = start_scheduler()