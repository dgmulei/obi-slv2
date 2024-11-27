"""Configuration and initialization utilities."""

import os
import yaml
import json
import logging
import tempfile
import streamlit as st
from typing import Dict, Any, TypedDict, List, Optional, cast
from dotenv import load_dotenv
from .conversation_manager import ConversationManager
from .embeddings_manager import EmbeddingsManager
from .query_engine import QueryEngine
from .chat_storage import ChatStorage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# ===== TYPE DEFINITIONS =====
class CommunicationPreferences(TypedDict):
    interaction_style: int  # 1 = highly methodical, 5 = highly efficient
    detail_level: int      # 1 = maximum context, 5 = minimal detail
    rapport_level: int     # 1 = highly personal, 5 = strictly professional

class UserProfile(TypedDict):
    personal: Dict[str, Any]
    addresses: Dict[str, Any]
    license: Dict[str, Any]
    documentation: Dict[str, Any]
    additional: Dict[str, Any]
    health: Dict[str, Any]
    payment: Dict[str, Any]
    metadata: Dict[str, Any]
    communication_preferences: CommunicationPreferences

class UserProfiles(TypedDict):
    users: List[UserProfile]

def setup_gcp_credentials() -> None:
    """Set up Google Cloud credentials from Streamlit secrets or local environment."""
    try:
        # First try to get credentials from environment variable
        if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            logger.info("Using GCP credentials from environment variable")
            return

        # Then try to use Streamlit secrets if available
        if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
            logger.info("Setting up GCP credentials from Streamlit secrets")
            # Create a temporary file to store the credentials
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                json.dump(dict(st.secrets['gcp_service_account']), f)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f.name
            logger.info("Successfully set up GCP credentials from Streamlit secrets")
            return

        # If neither is available, raise an error
        raise ValueError("No GCP credentials found in environment or Streamlit secrets")
    except Exception as e:
        logger.error(f"Failed to set up GCP credentials: {str(e)}")
        raise

def ensure_directories():
    """Ensure all required directories exist."""
    dirs = [
        os.getenv('CHROMA_DB_PATH', './chroma_db'),
        os.getenv('DOCUMENTS_PATH', './data/drivers_license_docs'),
        '.streamlit'
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Ensured directory exists: {dir_path}")

def load_user_profiles() -> UserProfiles:
    """Load user profiles from YAML file."""
    empty_profiles: UserProfiles = {"users": []}
    try:
        with open('user-profiles-yaml.txt', 'r') as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict) or 'users' not in data:
                return empty_profiles
            return cast(UserProfiles, data)
    except Exception as e:
        logger.error(f"Error loading user profiles: {e}")
        return empty_profiles

def get_processed_files_path() -> str:
    """Get the path to the processed files list."""
    db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
    return os.path.join(db_path, "processed_files.json")

def check_for_new_files() -> bool:
    """Check if there are any new files that need to be processed."""
    docs_dir = os.getenv('DOCUMENTS_PATH', './data/drivers_license_docs')
    processed_files_path = get_processed_files_path()
    
    # Get current text files
    text_files = set(f for f in os.listdir(docs_dir) if f.endswith('.txt'))
    
    # Get previously processed files
    processed_files = set()
    if os.path.exists(processed_files_path):
        try:
            with open(processed_files_path, 'r') as f:
                processed_files = set(json.load(f))
        except Exception as e:
            logger.warning(f"Error loading processed files list: {e}")
    
    # Check if there are any new files
    return bool(text_files - processed_files)

@st.cache_resource(show_spinner=False)
def get_embeddings_manager(_has_new_files: bool) -> EmbeddingsManager:
    """Get or create embeddings manager."""
    model_name = os.getenv('MODEL_NAME', 'all-MiniLM-L6-v2')
    db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
    return EmbeddingsManager(model_name=model_name, db_path=db_path)

@st.cache_resource
def get_chat_storage() -> Optional[ChatStorage]:
    """Initialize chat storage with proper error handling."""
    try:
        setup_gcp_credentials()
        bucket_name = os.getenv('GCS_BUCKET_NAME')
        if not bucket_name and hasattr(st, 'secrets'):
            bucket_name = st.secrets.get('GCS_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("GCS_BUCKET_NAME not found in environment or secrets")
        
        os.environ['GCS_BUCKET_NAME'] = bucket_name
        storage = ChatStorage()
        logger.info("Successfully initialized chat storage")
        return storage
    except Exception as e:
        logger.error(f"Failed to initialize chat storage: {str(e)}")
        return None

@st.cache_resource
def initialize_components(_differentiation_level: float):
    """Initialize components with differentiation level."""
    logger.info("Starting initialization...")
    ensure_directories()
    
    has_new_files = check_for_new_files()
    logger.info(f"New files detected: {has_new_files}")
    embeddings_manager = get_embeddings_manager(has_new_files)
    
    collection = embeddings_manager.get_collection()
    if collection is None:
        raise ValueError("Failed to initialize ChromaDB collection")
    
    query_engine = QueryEngine(collection=collection)
    
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    if not anthropic_api_key and hasattr(st, 'secrets'):
        anthropic_api_key = st.secrets.get('ANTHROPIC_API_KEY')
    if not anthropic_api_key:
        raise ValueError("Anthropic API key not found")
    
    chat_storage = get_chat_storage()
    
    conversation_manager = ConversationManager(
        query_engine=query_engine,
        api_key=anthropic_api_key,
        chat_storage=chat_storage,
        differentiation_level=_differentiation_level
    )
    
    return embeddings_manager, query_engine, conversation_manager
