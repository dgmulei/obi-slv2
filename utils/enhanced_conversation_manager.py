"""
EnhancedConversationManager module implementing a two-tier memory system using Langchain.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import logging
from anthropic import Anthropic
from langchain.memory import ConversationBufferMemory
from .style_calibrator import StyleCalibrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProjectFolder:
    """Represents the comprehensive context for a user session."""
    user_profile: Dict[str, Any]
    system_prompt: str
    calibrated_controls: Dict[str, Any]
    timestamp: datetime = datetime.now()

class EnhancedConversationManager:
    """
    Manages conversation flow using a two-tier memory system:
    Tier 1 (Project Folder): Comprehensive context set at session start
    Tier 2 (Ongoing Conversation): Current conversation focus
    """
    
    def __init__(self, api_key: str, differentiation_level: float = 75):
        """
        Initialize the enhanced conversation manager.
        
        Args:
            api_key: Anthropic API key
            differentiation_level: Level of style differentiation (0-100)
        """
        if not isinstance(api_key, str):
            raise ValueError("API key must be a string")
            
        self.api_key = api_key
        self.anthropic_client = Anthropic(api_key=api_key)
        self.style_calibrator = StyleCalibrator(differentiation_level)
        self.user_profile = None
        self.current_project_folder = None
        self.latest_calibration_message = None  # Store latest calibration message
        
        # Initialize project folder memory
        self.project_folder = ConversationBufferMemory(
            return_messages=True,
            memory_key="project_context"
        )
        
        # Track if session is initialized
        self.session_initialized = False
        self.system_prompt = None

    def update_differentiation_level(self, value: float) -> None:
        """
        Update the differentiation level and recalibrate values.
        
        Args:
            value: New differentiation level (0-100)
        """
        try:
            logger.info(f"Updating differentiation level to {value}")
            
            # Create new calibrator with updated level
            self.style_calibrator = StyleCalibrator(value)
            
            # If we have an active session, recalibrate and update project folder
            if self.session_initialized and self.user_profile:
                # Get newly calibrated controls
                calibrated_controls = self.style_calibrator.calibrate_structured_controls(
                    self.user_profile.get('metadata', {}).get('communication_controls', {})
                )
                
                # Update project folder with new calibrated values
                self.current_project_folder = ProjectFolder(
                    user_profile=self.user_profile,
                    system_prompt=self.system_prompt,
                    calibrated_controls=calibrated_controls
                )
                
                # Update system prompt with new calibrated values
                self._update_system_prompt()
                
                # Create and store latest calibration message
                self.latest_calibration_message = {
                    "role": "assistant",
                    "content": (
                        "[COMMUNICATION UPDATE] Please adjust your communication style according to these new preferences:\n"
                        f"- Interaction Style: {calibrated_controls['interaction_style']}\n"
                        f"- Detail Level: {calibrated_controls['detail_level']}\n"
                        f"- Rapport Level: {calibrated_controls['rapport_level']}\n\n"
                        "Apply these preferences to all subsequent responses."
                    )
                }
                
                logger.info("Successfully updated differentiation level and recalibrated values")
                
        except Exception as e:
            logger.error(f"Error updating differentiation level: {str(e)}")
            
    def _update_system_prompt(self) -> None:
        """Update system prompt with recalibrated values."""
        try:
            if not self.user_profile:
                return
                
            # Get calibrated communication controls
            calibrated_controls = self.style_calibrator.calibrate_structured_controls(
                self.user_profile.get('metadata', {}).get('communication_controls', {})
            )
            
            # Create comprehensive system message
            system_template = """SYSTEM RULES (NON-NEGOTIABLE):
- You are a professional guide helping Massachusetts citizens renew their driver's licenses
- Adapt your approach based on user profiles
- No exclamation points
- Each response must be directly related to the user's most recent message
- Only link to official RMV pages
- Step-by-step guidance if user shows confusion
- Protect sensitive information
- When you see a [COMMUNICATION UPDATE] message, immediately adjust your communication style

USER CONTEXT:
Name: {name}
License: {license_number} (Expires: {license_expiration})
Status: {restrictions}
Documentation: {documentation_format}
Special Notes: {special_notes}

COMMUNICATION PREFERENCES:
Interaction Style: {interaction_style}
Detail Level: {detail_level}
Rapport Level: {rapport_level}

USER PROFILE SUMMARY:
{bagman_description}

STRUCTURED COMMUNICATION REQUIREMENTS:
{structured_instructions}"""

            # Format system message with user context and calibrated values
            self.system_prompt = system_template.format(
                name=self.user_profile['personal']['full_name'],
                license_number=self.user_profile['license']['current']['number'],
                license_expiration=self.user_profile['license']['current']['expiration'],
                restrictions=', '.join(self.user_profile['license']['current'].get('restrictions', [])),
                documentation_format=self.user_profile['documentation'].get('preferred_format', 'standard'),
                special_notes=self.user_profile['license'].get('previous', {}).get('assisted_by', 'None'),
                interaction_style=calibrated_controls['interaction_style'],
                detail_level=calibrated_controls['detail_level'],
                rapport_level=calibrated_controls['rapport_level'],
                bagman_description=self.user_profile.get('metadata', {}).get('bagman_description', ''),
                structured_instructions=self._format_structured_instructions(calibrated_controls)
            )
            
            logger.info("System prompt updated with new calibrated values")
            
        except Exception as e:
            logger.error(f"Error updating system prompt: {str(e)}")
        
    def initialize_session(self, user_profile: Dict[str, Any]) -> None:
        """
        Initialize a new session with comprehensive context (Tier 1).
        
        Args:
            user_profile: Complete user profile including preferences
        """
        try:
            logger.info("Initializing session with user profile")
            
            # Store user profile for later recalibration
            self.user_profile = user_profile
            
            # Get initial calibrated controls
            calibrated_controls = self.style_calibrator.calibrate_structured_controls(
                user_profile.get('metadata', {}).get('communication_controls', {})
            )
            
            # Create initial project folder
            self.current_project_folder = ProjectFolder(
                user_profile=user_profile,
                system_prompt="",  # Will be set by _update_system_prompt
                calibrated_controls=calibrated_controls
            )
            
            # Initial system prompt creation
            self._update_system_prompt()
            
            # Update project folder with system prompt
            self.current_project_folder.system_prompt = self.system_prompt
            
            # Create initial calibration message
            self.latest_calibration_message = {
                "role": "assistant",
                "content": (
                    "[COMMUNICATION UPDATE] Initial communication preferences:\n"
                    f"- Interaction Style: {calibrated_controls['interaction_style']}\n"
                    f"- Detail Level: {calibrated_controls['detail_level']}\n"
                    f"- Rapport Level: {calibrated_controls['rapport_level']}\n\n"
                    "Please adjust your communication style accordingly."
                )
            }
            
            self.session_initialized = True
            logger.info(f"Session initialized for user: {user_profile['personal']['full_name']}")
            
        except Exception as e:
            logger.error(f"Failed to initialize session: {str(e)}", exc_info=True)
            raise
            
    def get_response(self, message: str) -> str:
        """
        Process a user message and generate a response (Tier 2).
        
        Args:
            message: The user's message
            
        Returns:
            str: The generated response
            
        Raises:
            RuntimeError: If session not initialized
        """
        if not self.session_initialized or not self.system_prompt:
            logger.error("Attempted to get response before session initialization")
            raise RuntimeError("Session must be initialized before getting responses")
            
        try:
            logger.info("Preparing request to Anthropic")
            
            # Create messages array with latest calibration if available
            messages = []
            if self.latest_calibration_message:
                messages.append(self.latest_calibration_message)
            messages.append({
                "role": "user",
                "content": message
            })
            
            logger.info("Sending request to Anthropic")
            
            # Generate response using Anthropic
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    messages=messages,
                    system=self.system_prompt,  # Pass system prompt separately
                    max_tokens=1024,
                    temperature=0.7
                )
                
                if not response.content:
                    logger.error("Empty response from Anthropic")
                    raise ValueError("Empty response from Anthropic")
                    
                logger.info("Successfully received response from Anthropic")
                return response.content[0].text
                
            except Exception as e:
                if "overloaded_error" in str(e):
                    logger.warning("Claude 3 Sonnet is overloaded, falling back to Claude 3 Opus")
                    response = self.anthropic_client.messages.create(
                        model="claude-3-opus-20240229",
                        messages=messages,
                        system=self.system_prompt,  # Pass system prompt separately
                        max_tokens=1024,
                        temperature=0.7
                    )
                    
                    if not response.content:
                        logger.error("Empty response from fallback model")
                        raise ValueError("Empty response from fallback model")
                        
                    logger.info("Successfully received response from fallback model")
                    return response.content[0].text
                else:
                    logger.error(f"Error from Anthropic API: {str(e)}", exc_info=True)
                    raise
                    
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            raise
            
    def _format_structured_instructions(self, controls: Dict[str, Any]) -> str:
        """Format structured communication controls into instructions."""
        try:
            instructions = []
            
            # Name/Title Usage
            if controls.get('title_required') and controls.get('professional_title'):
                instructions.append(f"- Address user as '{controls['professional_title']} {controls.get('preferred_name', '')}'")
            
            # Formality Level
            instructions.append(f"- Maintain {controls.get('formality_level', 'formal')} communication style")
            
            # Age Category
            age_cat = controls.get('age_category', 'adult')
            if age_cat == 'senior':
                instructions.append("- Use clear, simple language")
                instructions.append("- Provide step-by-step guidance")
            elif age_cat == 'youth':
                instructions.append("- Use straightforward explanations")
                instructions.append("- Avoid complex terminology")
                
            # Professional Status
            prof_status = controls.get('professional_status', 'none')
            if prof_status == 'active':
                instructions.append("- Prioritize efficiency in communication")
                instructions.append("- Focus on key points and action items")
            elif prof_status == 'retired':
                instructions.append("- Provide comprehensive explanations")
                instructions.append("- Allow time for questions and clarification")
                
            return "\n".join(instructions)
            
        except Exception as e:
            logger.error(f"Error formatting structured instructions: {str(e)}", exc_info=True)
            return "- Maintain professional communication style"
