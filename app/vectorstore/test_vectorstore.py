import logging
from app.vectorstore.collections import CollectionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test the CollectionManager
collection_name = "test_collection"
metadata = {"description": "Test collection"}

try:
    # Get or create a collection
    collection = CollectionManager.get_or_create_collection(
        name=collection_name,
        metadata=metadata
    )
    
    logger.info("Successfully created/retrieved collection: %s", collection_name)
    
    # Add some test data
    documents = ["This is a test document", "Another test document"]
    ids = ["id1", "id2"]
    
    collection.add(
        documents=documents,
        ids=ids
    )
    
    logger.info("Added test documents to collection")
    
    # Query the collection
    results = collection.query(
        query_texts=["test document"],
        n_results=2
    )
    
    logger.info("Query results: %s", results)
    
    # Clean up
    collection.delete(ids=ids)
    
    logger.info("Cleaned up test data")

except Exception as e:
    logger.error("Error testing vectorstore: %s", str(e))
    raise