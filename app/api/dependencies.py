"""
FastAPI dependency injection.
"""
from app.embeddings.embedding_factory import create_embedding_service
from app.vectorstore import get_vector_store
from app.rag.context_builder import ContextBuilder
from app.rag.retriever import Retriever
from app.llm.client import LLMClient
from app.rag.generator import Generator
from app.rag.pipeline import RAGPipeline
from app.services.document_service import DocumentService
from app.services.summary_service import SummaryService
from app.services.search_service import SearchService
from app.services.chat_service import ChatService
from app.config.settings import settings

_embed_service = None
_vector_store = None
_context_builder = None
_retriever = None
_llm_client = None
_generator = None
_rag_pipeline = None
_document_service = None
_summary_service = None
_search_service = None
_chat_service = None


def get_embed_service():
    global _embed_service
    if _embed_service is None:
        _embed_service = create_embedding_service()
    return _embed_service


def get_vector_store():
    global _vector_store
    if _vector_store is None:
        from app.vectorstore import get_vector_store as gvs
        _vector_store = gvs()
    return _vector_store


def get_context_builder():
    global _context_builder
    if _context_builder is None:
        _context_builder = ContextBuilder()
    return _context_builder


def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = Retriever(
            embed_service=get_embed_service(),
            vector_store=get_vector_store(),
            context_builder=get_context_builder(),
        )
    return _retriever


def get_llm_client():
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


def get_generator():
    global _generator
    if _generator is None:
        _generator = Generator(llm_client=get_llm_client())
    return _generator


def get_rag_pipeline():
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline(
            retriever=get_retriever(),
            generator=get_generator(),
        )
    return _rag_pipeline


def get_document_service():
    global _document_service
    if _document_service is None:
        _document_service = DocumentService(
            embed_service=get_embed_service(),
            vector_store=get_vector_store(),
            upload_dir=settings.UPLOAD_DIR,
        )
    return _document_service


def get_summary_service():
    global _summary_service
    if _summary_service is None:
        _summary_service = SummaryService(rag_pipeline=get_rag_pipeline())
    return _summary_service


def get_search_service():
    global _search_service
    if _search_service is None:
        _search_service = SearchService(retriever=get_retriever())
    return _search_service


def get_chat_service():
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService(rag_pipeline=get_rag_pipeline())
    return _chat_service