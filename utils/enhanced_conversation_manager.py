"""
EnhancedConversationManager module implementing conversation management with context intelligence.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging
from anthropic import Anthropic
from .style_calibrator import StyleCalibrator
from .communication_controller import CommunicationController

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProjectFolder:
    """Represents the comprehensive context for a user session."""
    user_profile: Dict[str, Any]
    system_prompt: str
    calibrated_controls: Dict[str, Any]
    latest_calibration_message: Optional[Dict[str, str]] = None

    def get_context_summary(self) -> str:
        """Get formatted summary of user context with prioritized information."""
        profile = self.user_profile
        summary = []

        # Critical License Information first
        if license_info := profile.get('license', {}).get('current', {}):
            summary.append("=== CRITICAL LICENSE INFORMATION ===")
            # Display all license fields in priority order
            if type_ := license_info.get('type'):
                summary.append(f"Type: {type_}")
            if purpose := license_info.get('purpose'):
                summary.append(f"Purpose: {purpose}")
            if expiration := license_info.get('expiration'):
                summary.append(f"EXPIRATION: {expiration}")
            if number := license_info.get('number'):
                summary.append(f"Number: {number}")
            if service := license_info.get('service'):
                summary.append(f"Service: {service}")
            
            # Add restrictions if present
            if restrictions := license_info.get('restrictions', []):
                summary.append(f"RESTRICTIONS: {', '.join(restrictions)}")
            
            # Add violations if present
            if violations := license_info.get('violations', []):
                summary.append("VIOLATIONS:")
                for violation in violations:
                    if isinstance(violation, dict):
                        v_type = violation.get('type', 'Unknown')
                        v_date = violation.get('date', 'No date')
                        v_fine = violation.get('fine')
                        v_status = violation.get('status', 'Unknown')
                        summary.append(f"- {v_type} ({v_date})")
                        if v_fine:
                            summary.append(f"  Fine: ${v_fine} - Status: {v_status}")
            summary.append("")

        # Documentation Status
        if docs := profile.get('documentation', {}):
            summary.append("=== DOCUMENTATION STATUS ===")
            for doc_type, doc_info in docs.items():
                if isinstance(doc_info, dict):
                    status = doc_info.get('status', 'Unknown')
                    expiry = doc_info.get('expiration', 'Not specified')
                    summary.append(f"{doc_type}: {status} (Expires: {expiry})")
                else:
                    summary.append(f"{doc_type}: {doc_info or 'Not specified'}")
            summary.append("")

        # Payment Information
        if payment := profile.get('payment', {}):
            summary.append("=== PAYMENT INFORMATION ===")
            if method := payment.get('method'):
                summary.append(f"Method: {method}")
            if auto_pay := payment.get('auto_pay'):
                summary.append(f"Auto-pay: {'Enabled' if auto_pay else 'Disabled'}")
            if check_number := payment.get('check_number'):
                summary.append(f"Check Number: {check_number}")
            
            if issues := payment.get('payment_issues', []):
                summary.append("Payment Issues:")
                for issue in issues:
                    summary.append(f"- {issue}")
            summary.append("")

        # Supporting Information
        if personal := profile.get('personal', {}):
            summary.append("=== PERSONAL INFORMATION ===")
            if name := personal.get('full_name'):
                summary.append(f"Name: {name}")
            if language := personal.get('primary_language'):
                summary.append(f"Language: {language}")
            if occupation := personal.get('occupation'):
                summary.append(f"Occupation: {occupation}")
            summary.append("")
            
        # Latest Communication Update
        if self.latest_calibration_message:
            summary.append("=== LATEST COMMUNICATION UPDATE ===")
            summary.append(self.latest_calibration_message['content'])
            summary.append("")

        return "\n".join(summary)

class EnhancedConversationManager:
    """
    Manages conversation flow with context intelligence scaling.
    Level 0-30: Mostly standardized responses
    Level 31-70: Begin incorporating preferences
    Level 71-100: Strictly adhere to preferences
    """
    
    def __init__(self, api_key: str, differentiation_level: float = 75):
        """Initialize with API key and differentiation level."""
        if not isinstance(api_key, str):
            raise ValueError("API key must be a string")
            
        self.api_key = api_key
        self.anthropic_client = Anthropic(api_key=api_key)
        self.style_calibrator = StyleCalibrator(differentiation_level)
        self.communication_controller = CommunicationController(differentiation_level)
        self.user_profile = None
        self.current_project_folder = None
        self.latest_calibration_message = None
        self.session_initialized = False
        self.system_prompt = None

    def _validate_profile(self, profile: Dict[str, Any]) -> bool:
        """Validate profile structure exists."""
        return isinstance(profile, dict)

    def _get_communication_preferences(self) -> Dict[str, Any]:
        """Get communication preferences in the correct structure."""
        if not self.user_profile:
            logger.warning("No user profile available")
            return {}
            
        # Get preferences from metadata
        preferences = self.user_profile.get('metadata', {}).get('communication_preferences', {})
        logger.info(f"Getting communication preferences: {preferences}")
        
        # Create properly structured dict
        return {
            'communication_preferences': preferences
        }

    def initialize_session(self, user_profile: Dict[str, Any]) -> None:
        """Initialize session with user profile."""
        try:
            # Log full profile for debugging
            logger.info("Initializing session with profile:")
            logger.info(f"Personal Info: {user_profile.get('personal', {})}")
            logger.info(f"Metadata: {user_profile.get('metadata', {})}")
            
            # Use profile as-is
            self.user_profile = user_profile
            
            # Get preferences in correct structure
            preferences = self._get_communication_preferences()
            logger.info(f"Using structured preferences: {preferences}")
            
            # Get calibrated controls
            calibrated_controls = self.style_calibrator.calibrate_structured_controls(preferences)
            logger.info(f"Calibrated Controls: {calibrated_controls}")
            
            self.current_project_folder = ProjectFolder(
                user_profile=user_profile,
                system_prompt="",
                calibrated_controls=calibrated_controls,
                latest_calibration_message=None
            )
            
            self._update_system_prompt()
            logger.info(f"Context summary: {self.current_project_folder.get_context_summary()}")
            
            self.session_initialized = True
            logger.info("Session initialized successfully")
                
        except Exception as e:
            logger.error(f"Session initialization failed: {str(e)}")
            raise

    def update_differentiation_level(self, value: float) -> None:
        """Update differentiation level and recalibrate."""
        try:
            logger.info(f"Updating differentiation level to {value}")
            
            self.style_calibrator = StyleCalibrator(value)
            self.communication_controller.update_differentiation_level(value)
            
            if self.session_initialized and self.user_profile:
                # Get preferences in correct structure
                preferences = self._get_communication_preferences()
                logger.info(f"Using structured preferences: {preferences}")
                
                # Get new calibrated controls
                calibrated_controls = self.style_calibrator.calibrate_structured_controls(preferences)
                logger.info(f"New calibrated controls: {calibrated_controls}")
                
                # Generate behavioral instructions
                style_instructions = self.communication_controller.generate_style_instructions(
                    calibrated_controls,
                    self.style_calibrator.differentiation_level
                )
                logger.info(f"Generated style instructions: {style_instructions}")
                
                # Create calibration message with behavioral instructions
                self.latest_calibration_message = {
                    "role": "assistant",
                    "content": f"[COMMUNICATION UPDATE] {style_instructions}"
                }
                
                # Update project folder with new controls and message
                self.current_project_folder = ProjectFolder(
                    user_profile=self.user_profile,
                    system_prompt=self.system_prompt,
                    calibrated_controls=calibrated_controls,
                    latest_calibration_message=self.latest_calibration_message
                )
                
                self._update_system_prompt()
                
        except Exception as e:
            logger.error(f"Error updating differentiation level: {str(e)}")
            raise

    def _get_license_info_display(self) -> str:
        """Get formatted license information for display."""
        if not self.user_profile:
            return "No license information available"

        if license_info := self.user_profile.get('license', {}).get('current', {}):
            parts = []

            # Critical information first
            if expiration := license_info.get('expiration'):
                parts.append(f"LICENSE EXPIRATION: {expiration}")

            if restrictions := license_info.get('restrictions', []):
                parts.append(f"RESTRICTIONS: {', '.join(restrictions)}")

            if violations := license_info.get('violations', []):
                parts.append("VIOLATIONS:")
                for violation in violations:
                    if isinstance(violation, dict):
                        v_type = violation.get('type', 'Unknown')
                        v_date = violation.get('date', 'No date')
                        fine = violation.get('fine')
                        parts.append(f"- {v_type} ({v_date})")
                        if fine:
                            parts.append(f"  Fine: ${fine}")

            if license_type := license_info.get('type'):
                parts.append(f"Type: {license_type}")

            return '\n'.join(parts)

        return "License information pending"
            
    def _update_system_prompt(self) -> None:
        """Update system prompt with prioritized context."""
        try:
            if not self.user_profile:
                return
                
            # Get preferences in correct structure
            preferences = self._get_communication_preferences()
            logger.info(f"Using structured preferences: {preferences}")
                
            calibrated_controls = self.style_calibrator.calibrate_structured_controls(preferences)
            logger.info(f"System prompt calibrated controls: {calibrated_controls}")
            
            system_template = """SYSTEM RULES:

You are a professional guide helping Massachusetts citizens renew their driver's licenses.
NEVER use exclamation points. 
Use natural questions to guide the conversation forward, ensuring they flow from the discussion rather than feeling tacked on. Your goal is to guide effectively, matching each user's preferred communication style.

INITIAL CONTACT GUIDELINES
1. Always keep the first response under 50 words and end with a question. 
2. First response must establish the following and be grounded in "bagman_description" insights:
- Appropriate formality level
- Tone
- Recognition of immediate needs
- Clear next step
- Brief qualifying question
3. NEVER give a numbered list or bullet list in the first response.

INFORMATION HANDLING:
1. Available Information:
    - State it confidently.
    - Adjust context based on user profile details, especially "bagman_description"
2. Partially Available Information:
    - Share what you know.
    - Tailor verification approach
3. Unavailable Information:
    - Acknowledge limitations transparently.
    - Focus on next steps.
    - Profile-based resource sharing, with a priority given to "bagman_description" insights
4. Complex Scenarios:
            - Collaborate with users by providing step-by-step guidance and connecting details from different sections when necessary.
            - Guide users to official verification when necessary.

TONE AND STYLE:
1. Never use exclamation points. Maintain a calm, professional tone that conveys confidence without excessive enthusiasm.
2. Adjust formality based on user profile, with a priority given to "bagman_description" insights.
3. Acknowledge user effort by describing their actions in a straightforward and professional manner, focusing on what they've done or are ready to do without overly praising or labeling behavior (e.g., avoid terms like "proactive").
4. Empathize with challenges based on user input, but avoid over-empathizing. For users who may value reassurance, offer calm and supportive guidance. For users who prefer efficiency, briefly acknowledge obstacles and move quickly to actionable solutions.
5. Avoid excessive praise, but offer practical encouragement to build confidence and keep users engaged.
6. Adjust the pacing and level of detail based on user preferences, with a priority given to "bagman_description" insights:

BEHAVIORAL GUIDANCE:
1. Use document information confidently when available.
2. Synthesize related information into one clear, actionable step at a time.
3. Frame solutions in user-specific terms that align with the user's needs and preferences, with a priority given to "bagman_description" insights.
4. Recommend helpful actions (e.g., scheduling appointments or gathering documents). Adapt recommendations to user preferences and personality traits. 
5. Present information for confirmation when needed.
6. If users express frustration or confusion, immediately switch to one-clear-step-at-a-time guidance.
7. Ensure accessibility for users with disabilities or special needs.
    
IMPORTANT:
- Monitor and alert on ALL restrictions and violations
- Flag ANY expired or expiring documents IMMEDIATELY
- Verify license status in EVERY interaction
- Check documentation requirements ALWAYS
- Consider payment preferences for transactions
- Provide clear step-by-step guidance
- Only link to official RMV pages
- Respect [COMMUNICATION UPDATE] instructions

ATTENTION REQUIREMENTS:
1. IMMEDIATE ACTION ITEMS:
   - Active restrictions or violations
   - Expired/expiring documents
   - License expiration status
   - Outstanding payments

2. VERIFICATION REQUIREMENTS:
   - Documentation completeness
   - Payment status
   - Eligibility criteria

3. GENERAL GUIDANCE:
   - Renewal procedures
   - Fee information
   - Location services
   - General inquiries

USER CONTEXT:
{context_summary}"""

            if self.current_project_folder:
                system_template = system_template.format(
                    context_summary=self.current_project_folder.get_context_summary()
                )
            
            self.system_prompt = system_template
            logger.info("System prompt updated with complete context")
            
        except Exception as e:
            logger.error(f"Error updating system prompt: {str(e)}")
            raise
            
    def get_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process message and generate response.
        
        Args:
            message: The user's message
            context: Optional context dictionary containing conversation history and markers
        """
        if not self.session_initialized:
            raise RuntimeError("Session must be initialized before getting responses")
            
        try:
            # Build message array with context
            messages = []
            
            # Include previous messages from context if available
            if context and 'previous_messages' in context:
                for prev_msg in context['previous_messages']:
                    if prev_msg.get('role') in ['user', 'assistant']:
                        messages.append({
                            "role": prev_msg['role'],
                            "content": prev_msg['content']
                        })
            
            # Include latest calibration message if available
            if self.latest_calibration_message and (not messages or messages[-1] != self.latest_calibration_message):
                messages.append(self.latest_calibration_message)
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Generate response
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    messages=messages,
                    system=self.system_prompt,
                    max_tokens=1024,
                    temperature=0.7
                )
                
                if not response.content:
                    raise ValueError("Empty response from Anthropic")
                
                return response.content[0].text
                
            except Exception as e:
                if "overloaded_error" in str(e):
                    logger.warning("Falling back to Claude 3 Opus")
                    response = self.anthropic_client.messages.create(
                        model="claude-3-opus-20240229",
                        messages=messages,
                        system=self.system_prompt,
                        max_tokens=1024,
                        temperature=0.7
                    )
                    
                    if not response.content:
                        raise ValueError("Empty response from fallback model")
                    
                    return response.content[0].text
                else:
                    raise
                    
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
