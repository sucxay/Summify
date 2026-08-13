from app.vectorstore.base import BaseVectorStore
from app.vectorstore.persistence import PersistenceManager
from app.vectorstore.search import similarity_search

class ChromaVectorStore(BaseVectorStore):

    def add_documents(self, chunks, embeddings):

        ids = [chunk.chunk_id for chunk in chunks]

        documents = [chunk.text for chunk in chunks]

        metadatas = [
            {
                "document_id": chunk.document_id,
                "page_start": chunk.page_start,
                "page_end": chunk.page_end,
                "chunk_index": chunk.chunk_index,
            }
            for chunk in chunks
        ]

        PersistenceManager.add_documents(
            collection_name=chunks[0].document_id,
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def similarity_search(self, query_embedding, top_k=5, filter=None):
        return similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
            metadata_filter=filter,
        )

    def delete_document(self, document_id):
        # implement later
        pass

    def count(self):
        # implement later
        return 0