"""
API router aggregation.
"""
from fastapi import APIRouter
from app.api.routes import health, documents, summary, search, chat

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(documents.router)
router.include_router(summary.router)
router.include_router(search.router)
router.include_router(chat.router)