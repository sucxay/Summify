"""
Summary generation endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.api.dependencies import get_summary_service
from app.services.summary_service import SummaryService

router = APIRouter(prefix="/summary", tags=["summary"])


class SummaryRequest(BaseModel):
    query: str
    document_id: Optional[str] = None
    summary_type: str = "general"
    top_k: int = 5


class SummaryResponse(BaseModel):
    query: str
    summary: str
    document_id: Optional[str]
    summary_type: str


@router.post("/", response_model=SummaryResponse)
async def generate_summary(
    request: SummaryRequest,
    summary_service: SummaryService = Depends(get_summary_service),
):
    valid_types = ["general", "executive", "bullet_points", "key_findings", "action_items"]
    if request.summary_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid summary type. Must be one of: {valid_types}",
        )

    result = summary_service.generate_summary(
        query=request.query,
        document_id=request.document_id,
        summary_type=request.summary_type,
        top_k=request.top_k,
    )
    return result


@router.post("/executive/{document_id}")
async def executive_summary(
    document_id: str,
    summary_service: SummaryService = Depends(get_summary_service),
):
    result = summary_service.generate_executive_summary(document_id)
    return result


@router.post("/bullets/{document_id}")
async def bullet_points(
    document_id: str,
    topic: Optional[str] = None,
    summary_service: SummaryService = Depends(get_summary_service),
):
    result = summary_service.generate_bullet_points(document_id, topic)
    return result


@router.post("/findings/{document_id}")
async def key_findings(
    document_id: str,
    summary_service: SummaryService = Depends(get_summary_service),
):
    result = summary_service.generate_key_findings(document_id)
    return result


@router.post("/actions/{document_id}")
async def action_items(
    document_id: str,
    summary_service: SummaryService = Depends(get_summary_service),
):
    result = summary_service.generate_action_items(document_id)
    return result