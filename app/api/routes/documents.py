"""
Document upload and management endpoints.
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pathlib import Path
import shutil

from app.api.dependencies import get_document_service
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    file_path = document_service.upload_dir / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    try:
        result = document_service.process_document(file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service),
):
    success = document_service.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "deleted", "document_id": document_id}


@router.get("/")
async def list_documents(
    document_service: DocumentService = Depends(get_document_service),
):
    documents = document_service.list_documents()
    return {"documents": documents, "total": len(documents)}