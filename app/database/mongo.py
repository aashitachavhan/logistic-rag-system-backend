from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.config import MONGODB_URL, DB_NAME, DOCUMENTS_COLLECTION
import logging

logger = logging.getLogger(__name__)

# Initialize MongoDB client
try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    # Verify connection
    client.admin.command('ping')
    logger.info("MongoDB connection established successfully")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    logger.warning(f"MongoDB connection failed: {e}. Some features may be unavailable.")
    client = None

def get_db():
    """Get database instance."""
    if client is None:
        logger.error("MongoDB client not initialized")
        return None
    return client[DB_NAME]

def get_documents_collection():
    """Get documents collection."""
    db = get_db()
    if db is None:
        return None
    return db[DOCUMENTS_COLLECTION]

def store_document_metadata(document_data):
    """
    Store document metadata in MongoDB.
    
    Args:
        document_data (dict): Dictionary containing:
            - filename (str)
            - upload_time (datetime)
            - is_logistics_document (bool)
            - extracted_preview (str)
    
    Returns:
        str: Inserted document ID (ObjectId) or None if insertion fails
    """
    try:
        collection = get_documents_collection()
        if collection is None:
            logger.error("Documents collection not available")
            return None
        
        result = collection.insert_one(document_data)
        logger.info(f"Document metadata stored: {document_data['filename']} (ID: {result.inserted_id})")
        return result.inserted_id
    except Exception as e:
        logger.error(f"Error storing document metadata: {e}")
        return None

def get_all_documents():
    """
    Retrieve all documents from the collection.
    
    Returns:
        list: List of documents (excluding the _id field from response)
    """
    try:
        collection = get_documents_collection()
        if collection is None:
            logger.error("Documents collection not available")
            return []
        
        documents = list(collection.find({}, {"_id": 0}))
        logger.info(f"Retrieved {len(documents)} documents from MongoDB")
        return documents
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return []
