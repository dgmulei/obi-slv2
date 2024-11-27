from typing import Optional, Dict, Any, List, Tuple, Literal
from dataclasses import dataclass, field
import logging
from datetime import datetime
import uuid
from anthropic import Anthropic
from .enhanced_conversation_manager import EnhancedConversationManager
from .communication_controller import CommunicationController

logger = logging.getLogger(__name__)

@dataclass
class Message:
    """Represents a single message in a conversation."""
    role: Literal["system", "user", "assistant"]
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    visible: bool = True

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return self.role == other.role and self.content == other.content

    def __hash__(self):
        return hash((self.role, self.content))

@dataclass
class ConversationContext:
    """Stores context for a conversation."""
    messages: List[Message] = field(default_factory=list)
    system_message_added: bool = False
    active_user_profile: Optional[Dict[str, Any]] = None
    user_profile: Optional[Dict[str, Any]] = None
    thread_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    needs_refresh: bool = False  # New flag to track UI refresh needs

class SessionManager:
    """Manages conversation sessions."""
    def __init__(self):
        self.active_sessions: Dict[str, ConversationContext] = {}
        self.enhanced_managers: Dict[str, EnhancedConversationManager] = {}
    
    def create_session(self, session_id: str, user_profile: Optional[Dict[str, Any]] = None) -> None:
        """Create a new conversation session."""
        self.active_sessions[session_id] = ConversationContext(user_profile=user_profile)
    
    def get_session(self, session_id: str) -> Optional[ConversationContext]:
        """Retrieve an existing conversation session."""
        return self.active_sessions.get(session_id)
    
    def end_session(self, session_id: str) -> None:
        """End and remove a conversation session."""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        if session_id in self.enhanced_managers:
            del self.enhanced_managers[session_id]

class ConversationManager:
    """Manages conversation flow and system prompts."""
    def __init__(self, query_engine, api_key: str, chat_storage=None, differentiation_level: float = 75, system_prompt: str = ""):
        """Initialize conversation manager with enhanced capabilities."""
        if not isinstance(api_key, str):
            raise ValueError("API key must be a string")
            
        self.query_engine = query_engine
        self.api_key = api_key
        self.chat_storage = chat_storage
        self.system_prompt = system_prompt
        self._differentiation_level = differentiation_level
        self.session_manager = SessionManager()
        self.communication_controller = CommunicationController()

    @property
    def differentiation_level(self) -> float:
        return self._differentiation_level

    @differentiation_level.setter
    def differentiation_level(self, value: float):
        """Update differentiation level and propagate to all enhanced managers."""
        if self._differentiation_level == value:
            return  # No change needed
            
        self._differentiation_level = value
        logger.info(f"Updating differentiation level to {value}")
        
        # Update all active enhanced managers and mark contexts for refresh
        for thread_id, enhanced_manager in self.session_manager.enhanced_managers.items():
            try:
                enhanced_manager.update_differentiation_level(value)
                # Mark the corresponding context for refresh
                if thread_id in self.session_manager.active_sessions:
                    self.session_manager.active_sessions[thread_id].needs_refresh = True
            except Exception as e:
                logger.error(f"Error updating enhanced manager for thread {thread_id}: {str(e)}")

    def get_response(self, message: str, context: ConversationContext, visible: bool = True) -> Tuple[str, bool]:
        """
        Process a user message and generate a response using the enhanced system.
        
        Args:
            message: The user's message
            context: The conversation context
            visible: Whether the message should be visible in the chat interface
        
        Returns:
            Tuple of (response text, success boolean)
        """
        try:
            logger.info(f"Processing message for thread {context.thread_id}")
            
            # Get or create enhanced manager for this session
            enhanced_manager = self.session_manager.enhanced_managers.get(context.thread_id)
            
            if not enhanced_manager:
                logger.info("Creating new enhanced manager")
                # Create new enhanced manager
                enhanced_manager = EnhancedConversationManager(
                    api_key=self.api_key,
                    differentiation_level=self._differentiation_level
                )
                
                # Initialize session with user profile
                if context.active_user_profile:
                    logger.info("Initializing session with active user profile")
                    try:
                        enhanced_manager.initialize_session(context.active_user_profile)
                    except Exception as e:
                        logger.error(f"Failed to initialize session: {str(e)}", exc_info=True)
                        return "I apologize, but I encountered an error initializing the session.", False
                else:
                    logger.error("No active user profile found in context")
                    return "I apologize, but I couldn't find the user profile information.", False
                    
                # Store manager for future use
                self.session_manager.enhanced_managers[context.thread_id] = enhanced_manager
            
            # Reset needs_refresh flag before processing
            context.needs_refresh = False
            
            # Get response using enhanced manager
            try:
                logger.info("Getting response from enhanced manager")
                response_content = enhanced_manager.get_response(message)
                
                # Store in chat history if storage is available
                if self.chat_storage and visible:
                    try:
                        # Format messages for storage
                        messages_for_storage = [
                            {
                                "role": "user",
                                "content": message,
                                "timestamp": datetime.now().isoformat() + "Z",
                                "visible": visible
                            },
                            {
                                "role": "assistant",
                                "content": response_content,
                                "timestamp": datetime.now().isoformat() + "Z",
                                "visible": visible
                            }
                        ]
                        
                        # Update thread in storage
                        self.chat_storage.update_thread(context.thread_id, messages_for_storage)
                        
                    except Exception as e:
                        logger.error(f"Failed to store chat history: {str(e)}", exc_info=True)
                
                return response_content, True
                
            except Exception as e:
                logger.error(f"Error getting response from enhanced manager: {str(e)}", exc_info=True)
                return "I apologize, but I encountered an error processing your request.", False
            
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}", exc_info=True)
            return "I apologize, but I encountered an error processing your request.", False
