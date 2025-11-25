"""Refactored FastAPI application for Band Music conversion platform."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.api import api_router
from src.config.settings import settings
from src.core.container import get_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Band Music API")
    logger.info(f"Upload directory: {settings.upload_dir}")
    logger.info(f"Output directory: {settings.output_dir}")
    
    # Initialize container (ensures all directories exist)
    container = get_container()
    logger.info("Dependency container initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Band Music API")


def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title="Band Music API",
        description="Convert sheet music images to audio and audio files to sheet music",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(api_router, prefix="/api")
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Band Music API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/health"
        }
    
    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_refactored:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
