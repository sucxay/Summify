import logging 
from app.vectorstore.collections import Collections 

logger  = logging.getLogger(__name__)

class PersistenceManager:
    @staticmethod
    def add_documents(
        collection_name:str , ids:list[str] ,documents:list[str] , metadatas:list[dict],embeddings:list[dict] |None = None
    )->None:
        """
        add documents to a collection with the given name, ids, documents, metadatas and embeddings.
        """
        collections = Collections.get_or_create_collection(name=collection_name)
        collections.add(ids = ids , documents = documents , metadatas = metadatas , embeddings = embeddings)
        logger.info('Added %d documents to collection %s.', len(documents), collection_name)
         
    @staticmethod
    def delete_documents(collection_name:str , ids:list[str])->None:

        collections  = Collections.get_collection(name= collection_name)

        collections.delete(ids = ids)

            
        logger.info('Deleted %d documents from collection %s.', len(ids), collection_name)



    @staticmethod
    def update_documents(collection_name:str , ids:list[str] , documents:list[str] , metadatas:list[dict],embeddings:list[dict] |None = None)->None:
        """
        update documents in a collection with the given name, ids, documents, metadatas and embeddings.
        """
        collections  = Collections.get_collection(name= collection_name)

        collections.update(ids = ids , documents = documents , metadatas = metadatas , embeddings = embeddings)
        
        logger.info('Updated %d documents in collection %s.', len(documents), collection_name)
       

    @staticmethod
    def upsert_documents(collection_name:str , ids:list[str] , documents:list[str] , metadatas:list[dict],embeddings:list[dict] |None = None)->None:
        """
        upsert documents in a collection with the given name, ids, documents, metadatas and embeddings.
        """
        collections  = Collections.get_collection(name= collection_name)

        collections.upsert(ids = ids , documents = documents , metadatas = metadatas , embeddings = embeddings)
        
        logger.info('Upserted %d documents in collection %s.', len(documents), collection_name) 

