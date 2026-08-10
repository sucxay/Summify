import logging 
from app.vectorstore.chroma import ChromaClient
from chromadb.api.models.Collection import Collection

logger = logging.getLogger(__name__)

class CollectionManager:
    @staticmethod
    def get_or_create_collection(name: str, metadata: dict | None = None) -> Collection:
        """
        Get or create a collection with the given name and metadata.
        """
        client = ChromaClient.get_client()

        collections = client.get_or_create_collection(name=name, metadata=metadata)

        logger.info('collection %s created or retrieved.', name)

        return collections
    @staticmethod
    def get_collection(name:str)->Collection:
        """
        get an existing collection with the given name."""

        client =ChromaClient.get_client()
        return client.get_collection(name=name)
    
    @staticmethod
    def delete_collection(name:str)-> None:
        """
        delete an existing collection with the given name.
        """
        client = ChromaClient.get_client()
        client.delete_collection(name=name)
        logger.info('collection %s deleted.', name)

    @staticmethod
    def list_collections()->list[str]:
        """
        list all existing collections.
        """
        client = ChromaClient.get_client()
        return client.list_collections()
