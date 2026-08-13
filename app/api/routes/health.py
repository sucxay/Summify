"""
Health check endpoint.
"""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "summify"}


@router.get("/health/ready")
async def readiness_check():
    return {"status": "ready"}