import chromadb
from chromadb.config import Settings as ChromaSettings
import logging 

from app.config.settings import settings



logger = logging.getLogger(__name__)

class ChromaClient:
    _client = None 

    @classmethod
    def get_client(cls): #persistant client runs locally on our machine.

        if cls._client is None: 
            cls._client = chromadb.PersistentClient(path = str(settings.CHROMA_DB_PATH), settings = ChromaSettings(anonymized_telemetry=False))

            return cls._client 
        
    @classmethod 
    def reset(cls):
        cls._client= None

        logger.warning('ChromaDB client reset.')

