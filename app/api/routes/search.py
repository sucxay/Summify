from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.api.dependencies import get_search_service
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])


class SearchRequest(BaseModel):
    query: str
    document_id: Optional[str] = None
    top_k: int = 5
    min_score: float = 0.0


class PageSearchRequest(BaseModel):
    query: str
    document_id: str
    page_start: int
    page_end: int
    top_k: int = 5


@router.post("/")
async def search(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service),
):
    result = search_service.search(
        query=request.query,
        top_k=request.top_k,
        document_id=request.document_id,
        min_score=request.min_score,
    )
    return result


@router.post("/pages")
async def search_pages(
    request: PageSearchRequest,
    search_service: SearchService = Depends(get_search_service),
):
    result = search_service.search_by_page_range(
        query=request.query,
        document_id=request.document_id,
        page_start=request.page_start,
        page_end=request.page_end,
        top_k=request.top_k,
    )
    return result