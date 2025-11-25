"""API routers package."""
from fastapi import APIRouter

from src.api.routes import omr, amt, health

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(omr.router, prefix="/omr", tags=["omr"])
api_router.include_router(amt.router, prefix="/amt", tags=["amt"])
