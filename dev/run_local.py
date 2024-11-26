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
import streamlit as st
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup environment variables and paths for local development."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Ensure required directories exist
    dirs = [
        os.getenv('CHROMA_DB_PATH', './chroma_db'),
        os.getenv('DOCUMENTS_PATH', './data/drivers_license_docs'),
        '.streamlit'
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Ensured directory exists: {dir_path}")

    # Verify critical environment variables
    required_vars = ['ANTHROPIC_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

def init_components():
    """Initialize all required components for the application."""
    from utils.embeddings_manager import EmbeddingsManager
    from utils.query_engine import QueryEngine
    from utils.conversation_manager import ConversationManager
    
    try:
        # Initialize EmbeddingsManager
        model_name = os.getenv('MODEL_NAME', 'all-MiniLM-L6-v2')
        db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
        embeddings_manager = EmbeddingsManager(model_name=model_name, db_path=db_path)
        logger.info("Successfully initialized EmbeddingsManager")
        
        # Get collection from embeddings manager
        collection = embeddings_manager.get_collection()
        if collection is None:
            raise ValueError("Failed to initialize ChromaDB collection")
        
        # Initialize QueryEngine with collection
        query_engine = QueryEngine(collection=collection)
        logger.info("Successfully initialized QueryEngine")
        
        # Initialize ConversationManager
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not anthropic_api_key:
            raise ValueError("Anthropic API key not found")
        conversation_manager = ConversationManager(
            query_engine=query_engine,
            api_key=anthropic_api_key
        )
        logger.info("Successfully initialized ConversationManager")
        
        return embeddings_manager, query_engine, conversation_manager
        
    except Exception as e:
        logger.error(f"Error during component initialization: {str(e)}")
        raise

def main():
    """Main entry point for local development."""
    try:
        # Setup environment
        setup_environment()
        logger.info("Environment setup complete")
        
        # Initialize components
        embeddings_manager, query_engine, conversation_manager = init_components()
        logger.info("Component initialization complete")
        
        # Import and run the main application
        import app
        app.main()
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

if __name__ == "__main__":
    main()
