import logging
from typing import Optional, List, Dict
from app.vectorstore.chroma import ChromaClient
from chromadb.api.models.Collection import Collection

logger = logging.getLogger(__name__)

class CollectionManager:
    """Manager for ChromaDB collections with CRUD operations."""

    @staticmethod
    def get_or_create_collection(
        name: str,
        metadata: Optional[Dict] = None
    ) -> Collection:
        """
        Get or create a collection with the given name and metadata.

        Args:
            name: Name of the collection
            metadata: Optional metadata dictionary

        Returns:
            Collection object
        """
        try:
            client = ChromaClient.get_client()
            collection = client.get_or_create_collection(name=name, metadata=metadata)
            logger.info('Collection %s created or retrieved.', name)
            return collection
        except Exception as e:
            logger.error('Failed to get or create collection %s: %s', name, e)
            raise

    @staticmethod
    def get_collection(name: str) -> Collection:
        """
        Get an existing collection with the given name.

        Args:
            name: Name of the collection

        Returns:
            Collection object

        Raises:
            ValueError: If collection doesn't exist
        """
        try:
            client = ChromaClient.get_client()
            return client.get_collection(name=name)
        except Exception as e:
            logger.error('Failed to get collection %s: %s', name, e)
            raise

    @staticmethod
    def delete_collection(name: str) -> None:
        """
        Delete an existing collection with the given name.

        Args:
            name: Name of the collection to delete
        """
        try:
            client = ChromaClient.get_client()
            client.delete_collection(name=name)
            logger.info('Collection %s deleted.', name)
        except Exception as e:
            logger.error('Failed to delete collection %s: %s', name, e)
            raise

    @staticmethod
    def list_collections() -> List[str]:
        """
        List all existing collection names.

        Returns:
            List of collection names
        """
        try:
            client = ChromaClient.get_client()
            return [c.name for c in client.list_collections()]
        except Exception as e:
            logger.error('Failed to list collections: %s', e)
            raise
