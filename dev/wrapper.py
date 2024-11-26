#!/usr/bin/env python3

# Add project root to Python path
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Patch SQLite before any other imports
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

from dotenv import load_dotenv
import logging
from typing import Tuple, Optional, Dict, Any
from pathlib import Path
from utils.query_engine import QueryEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_env(env_path: Optional[str] = None) -> Dict[str, str]:
    """
    Load environment variables from .env file.
    
    Args:
        env_path: Optional path to .env file. If not provided, searches in current directory.
    
    Returns:
        Dict of loaded environment variables
    """
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()
    
    # Verify and return critical environment variables
    required_vars = ['ANTHROPIC_API_KEY', 'CHROMA_DB_PATH', 'DOCUMENTS_PATH']
    env_vars = {}
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            logger.warning(f"Missing environment variable: {var}")
        env_vars[var] = value or ''
    
    return env_vars

def init_embeddings_manager(model_name: Optional[str] = None, db_path: Optional[str] = None):
    """
    Initialize EmbeddingsManager in isolation.
    
    Args:
        model_name: Optional model name for SentenceTransformer
        db_path: Optional path for ChromaDB storage
    
    Returns:
        Initialized EmbeddingsManager instance
    """
    from utils.embeddings_manager import EmbeddingsManager
    
    model = model_name or os.getenv('MODEL_NAME', 'all-MiniLM-L6-v2')
    path = db_path or os.getenv('CHROMA_DB_PATH', './chroma_db')
    
    return EmbeddingsManager(model_name=model, db_path=path)

def init_query_engine(collection=None):
    """
    Initialize QueryEngine in isolation.
    
    Args:
        collection: Optional ChromaDB collection. If not provided, creates new one.
    
    Returns:
        Initialized QueryEngine instance
    """
    if collection is None:
        embeddings_manager = init_embeddings_manager()
        collection = embeddings_manager.get_collection()
    
    return QueryEngine(collection=collection)

def init_conversation_manager(query_engine=None, api_key: Optional[str] = None):
    """
    Initialize ConversationManager in isolation.
    
    Args:
        query_engine: Optional QueryEngine instance
        api_key: Optional Anthropic API key
    
    Returns:
        Initialized ConversationManager instance
    """
    from utils.conversation_manager import ConversationManager
    
    if query_engine is None:
        query_engine = init_query_engine()
    
    key = api_key or os.getenv('ANTHROPIC_API_KEY')
    if not key:
        raise ValueError("Anthropic API key not found")
    
    return ConversationManager(query_engine=query_engine, api_key=key)

def init_all_components() -> Tuple[Any, Any, Any]:
    """
    Initialize all components together.
    
    Returns:
        Tuple of (EmbeddingsManager, QueryEngine, ConversationManager)
    """
    # Load environment variables
    load_env()
    
    # Initialize components
    embeddings_manager = init_embeddings_manager()
    collection = embeddings_manager.get_collection()
    query_engine = QueryEngine(collection=collection)
    conversation_manager = init_conversation_manager(query_engine=query_engine)
    
    return embeddings_manager, query_engine, conversation_manager

def ensure_directories() -> None:
    """Ensure all required directories exist."""
    dirs = [
        os.getenv('CHROMA_DB_PATH', './chroma_db'),
        os.getenv('DOCUMENTS_PATH', './data/drivers_license_docs'),
        '.streamlit'
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Ensured directory exists: {dir_path}")

def test_component_initialization() -> bool:
    """
    Test initialization of all components.
    
    Returns:
        True if all components initialize successfully, False otherwise
    """
    try:
        embeddings_manager, query_engine, conversation_manager = init_all_components()
        logger.info("All components initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error during component initialization: {str(e)}")
        return False
