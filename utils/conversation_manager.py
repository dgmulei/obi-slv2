from typing import Optional, Dict, Any, List, Tuple, Literal
from dataclasses import dataclass, field
import logging
from datetime import datetime
import uuid
import json
from anthropic import Anthropic
from .enhanced_conversation_manager import EnhancedConversationManager
from .communication_controller import CommunicationController

logger = logging.getLogger(__name__)

@dataclass
class ConversationMarkers:
    """Tracks specific conversation elements that need persistence."""
    numbered_lists: List[List[str]] = field(default_factory=list)
    reference_points: List[Dict[str, Any]] = field(default_factory=list)
    key_details: Dict[str, Any] = field(default_factory=dict)

    def add_numbered_list(self, items: List[str]) -> None:
        """Add a new numbered list to track."""
        self.numbered_lists.append(items)

    def add_reference_point(self, reference: Dict[str, Any]) -> None:
        """Add a new reference point from the conversation."""
        self.reference_points.append(reference)

    def add_key_detail(self, key: str, value: Any) -> None:
        """Add a key detail to track."""
        self.key_details[key] = value

@dataclass
class Message:
    """Represents a single message in a conversation."""
    role: Literal["system", "user", "assistant"]
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    visible: bool = True
    context_markers: Optional[ConversationMarkers] = None

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
    needs_refresh: bool = False
    conversation_markers: ConversationMarkers = field(default_factory=ConversationMarkers)
    
    def add_message(self, message: Message) -> None:
        """Add a message while maintaining context."""
        # Skip "Hello?" messages
        if message.role == "user" and message.content.strip().lower() == "hello?":
            return
            
        self.messages.append(message)
        
        # Extract and track numbered lists
        if "1." in message.content:
            items = []
            for line in message.content.split('\n'):
                if line.strip().startswith(tuple(f"{i}." for i in range(1, 10))):
                    items.append(line.strip())
            if items:
                self.conversation_markers.add_numbered_list(items)

        # Track key details mentioned in the message
        if message.role == "assistant":
            # Track specific details that might need reference later
            if "license" in message.content.lower():
                self.conversation_markers.add_key_detail("license_mentioned", True)
            if "document" in message.content.lower():
                self.conversation_markers.add_key_detail("documents_discussed", True)

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get formatted conversation history with context."""
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "context_markers": msg.context_markers.__dict__ if msg.context_markers else None
            }
            for msg in self.messages
        ]

    def validate_context(self) -> bool:
        """Validate context completeness and consistency."""
        if not self.active_user_profile:
            logger.error("Missing active user profile in context")
            return False
        return True

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

    def prepare_context(self, context: ConversationContext, message: str) -> Dict[str, Any]:
        """Prepare complete context for response generation."""
        # Ensure all data is JSON serializable
        context_data = {
            'previous_messages': context.get_conversation_history(),
            'current_message': message,
            'profile_data': context.active_user_profile,
            'conversation_markers': context.conversation_markers.__dict__,
            'differentiation_level': self._differentiation_level
        }
        # Convert to JSON and back to ensure everything is serializable
        return json.loads(json.dumps(context_data, default=str))

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
            
            # Validate context before proceeding
            if not context.validate_context():
                return "I apologize, but I'm missing some important context to properly assist you.", False
            
            # Skip adding "Hello?" to context but still process it
            if message.strip().lower() != "hello?":
                # Add user message to context
                user_message = Message(role="user", content=message, visible=visible)
                context.add_message(user_message)
            
            # Get or create enhanced manager for this session
            enhanced_manager = self.session_manager.enhanced_managers.get(context.thread_id)
            
            if not enhanced_manager:
                logger.info("Creating new enhanced manager")
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
                    
                self.session_manager.enhanced_managers[context.thread_id] = enhanced_manager
            
            # Prepare complete context for response generation
            complete_context = self.prepare_context(context, message)
            
            # Reset needs_refresh flag before processing
            context.needs_refresh = False
            
            try:
                logger.info("Getting response from enhanced manager")
                response_content = enhanced_manager.get_response(message, complete_context)
                
                # Add assistant response to context
                assistant_message = Message(
                    role="assistant",
                    content=response_content,
                    visible=visible,
                    context_markers=ConversationMarkers()
                )
                context.add_message(assistant_message)
                
                # Store in chat history if storage is available
                if self.chat_storage and visible:
                    try:
                        messages_for_storage = [
                            {
                                "role": "user",
                                "content": message,
                                "timestamp": datetime.now().isoformat() + "Z",
                                "visible": visible,
                                "context": complete_context
                            },
                            {
                                "role": "assistant",
                                "content": response_content,
                                "timestamp": datetime.now().isoformat() + "Z",
                                "visible": visible,
                                "context": complete_context
                            }
                        ]
                        
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
