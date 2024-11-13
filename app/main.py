from fastapi import FastAPI
import uvicorn
from .routers import articles
from .database import engine, Base
import asyncio
# Create all tables
# Note: For async engine, you need to use an async context


app = FastAPI(
    title="News Tracker API",
    description="API to track changes in online news articles over time.",
    version="0.1.0",
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app.include_router(articles.router)