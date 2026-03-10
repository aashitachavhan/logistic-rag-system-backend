from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.config import MONGODB_URL, DB_NAME, DOCUMENTS_COLLECTION
import logging

logger = logging.getLogger(__name__)

CHAT_SESSIONS_COLLECTION = "chat_sessions"

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

def get_chat_sessions_collection():
    """Get chat sessions collection."""
    db = get_db()
    if db is None:
        return None
    return db[CHAT_SESSIONS_COLLECTION]

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
        logger.info(f"Retrieved {len} documents from MongoDB")
        return documents
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return []
def delete_document_by_filename(filename: str) -> bool:
    """
    Delete a document from MongoDB by its filename.
    
    Args:
        filename (str): The filename of the document to delete
    
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        collection = get_documents_collection()
        if collection is None:
            logger.error("Documents collection not available")
            return False
        
        result = collection.delete_one({"filename": filename})
        if result.deleted_count > 0:
            logger.info(f"Document deleted from MongoDB: {filename}")
            return True
        else:
            logger.warning(f"Document not found in MongoDB: {filename}")
            return False
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        return False
def delete_document_metadata(filename):
    """
    Delete document metadata from MongoDB by filename.
    
    Args:
        filename (str): The filename of the document to delete.
    
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        collection = get_documents_collection()
        if collection is None:
            logger.error("Documents collection not available")
            return False
        
        result = collection.delete_one({"filename": filename})
        if result.deleted_count > 0:
            logger.info(f"Document metadata deleted: {filename}")
            return True
        else:
            logger.warning(f"No document found with filename: {filename}")
            return False
    except Exception as e:
        logger.error(f"Error deleting document metadata: {e}")
        return False


# Chat Sessions Functions

def create_chat_session(session_data):
    """
    Create a new chat session in MongoDB.
    
    Args:
        session_data (dict): Dictionary containing session data.
    
    Returns:
        str: Inserted document ID or None if failed.
    """
    try:
        collection = get_chat_sessions_collection()
        if collection is None:
            logger.error("Chat sessions collection not available")
            return None
        
        result = collection.insert_one(session_data)
        logger.info(f"Chat session created: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error creating chat session: {e}")
        return None


def get_all_chat_sessions():
    """
    Retrieve all chat sessions.
    
    Returns:
        list: List of chat sessions.
    """
    try:
        collection = get_chat_sessions_collection()
        if collection is None:
            logger.error("Chat sessions collection not available")
            return []
        
        sessions = list(collection.find({}, {"_id": 1, "session_title": 1, "created_at": 1}))
        for session in sessions:
            session["id"] = str(session.pop("_id"))
        return sessions
    except Exception as e:
        logger.error(f"Error retrieving chat sessions: {e}")
        return []


def get_chat_session_by_id(session_id):
    """
    Retrieve a chat session by ID.
    
    Args:
        session_id (str): The session ID.
    
    Returns:
        dict: The chat session or None.
    """
    try:
        collection = get_chat_sessions_collection()
        if collection is None:
            logger.error("Chat sessions collection not available")
            return None
        
        from bson import ObjectId
        session = collection.find_one({"_id": ObjectId(session_id)})
        if session:
            session["id"] = str(session.pop("_id"))
        return session
    except Exception as e:
        logger.error(f"Error retrieving chat session: {e}")
        return None


def update_chat_session(session_id, update_data):
    """
    Update a chat session.
    
    Args:
        session_id (str): The session ID.
        update_data (dict): Data to update.
    
    Returns:
        bool: True if updated, False otherwise.
    """
    try:
        collection = get_chat_sessions_collection()
        if collection is None:
            logger.error("Chat sessions collection not available")
            return False
        
        from bson import ObjectId
        result = collection.update_one({"_id": ObjectId(session_id)}, {"$set": update_data})
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error updating chat session: {e}")
        return False


def delete_chat_session(session_id):
    """
    Delete a chat session.
    
    Args:
        session_id (str): The session ID.
    
    Returns:
        bool: True if deleted, False otherwise.
    """
    try:
        collection = get_chat_sessions_collection()
        if collection is None:
            logger.error("Chat sessions collection not available")
            return False
        
        from bson import ObjectId
        result = collection.delete_one({"_id": ObjectId(session_id)})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error deleting chat session: {e}")
        return False
