"""
CommunicationController module for managing response modifications based on context level.
"""

from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommunicationController:
    """
    Controls response modifications based on differentiation level.
    Level 0-30: Mostly standardized responses
    Level 31-70: Begin incorporating preferences
    Level 71-100: Strictly adhere to preferences
    """
    
    def __init__(self, differentiation_level: float = 75.0):
        """Initialize with differentiation level."""
        if not 0 <= differentiation_level <= 100:
            raise ValueError("differentiation_level must be between 0 and 100")
            
        self._differentiation_level = differentiation_level
        self._last_calibrated_values: Optional[Dict[str, float]] = None
        logger.info(f"CommunicationController initialized with differentiation_level: {differentiation_level}")
        
    @property
    def differentiation_level(self) -> float:
        """Get the current differentiation level."""
        return self._differentiation_level
        
    def update_differentiation_level(self, value: float) -> None:
        """Update the differentiation level."""
        if not 0 <= value <= 100:
            raise ValueError("differentiation_level must be between 0 and 100")
        self._differentiation_level = value
        logger.info(f"Updated differentiation level to {value}")
    
    def generate_style_instructions(self, controls: Dict[str, Any], level: float) -> str:
        """
        Generate behavioral style instructions for Claude based on calibrated controls and level.
        """
        try:
            # Store calibrated values for Case File display
            self._last_calibrated_values = {
                'interaction_style': controls.get('interaction_style', 3),
                'detail_level': controls.get('detail_level', 3),
                'rapport_level': controls.get('rapport_level', 3)
            }
            
            instructions = []
            
            # Core style parameters
            instructions.append("Please adjust your communication style:")
            instructions.append(f"• Interaction Style: {self._last_calibrated_values['interaction_style']}")
            instructions.append(f"• Detail Level: {self._last_calibrated_values['detail_level']}")
            instructions.append(f"• Rapport Level: {self._last_calibrated_values['rapport_level']}")
            
            # Add behavioral guidance based on level
            instructions.append("\nBehavioral Guidance:")
            
            # Interaction Style Instructions (1=methodical to 5=efficient)
            interaction_style = self._last_calibrated_values['interaction_style']
            if interaction_style <= 2:
                instructions.append(
                    "• Provide methodical, step-by-step guidance"
                    "\n• Break down complex topics into manageable steps"
                )
            elif interaction_style >= 4:
                instructions.append(
                    "• Be efficient and direct"
                    "\n• Focus on key points without unnecessary elaboration"
                )
            else:
                instructions.append(
                    "• Balance step-by-step guidance with efficient delivery"
                    "\n• Provide clear structure while maintaining conciseness"
                )
                
            # Detail Level Instructions (1=maximum to 5=minimal)
            detail_level = self._last_calibrated_values['detail_level']
            if detail_level <= 2:
                instructions.append(
                    "• Provide comprehensive explanations"
                    "\n• Include relevant background information"
                )
            elif detail_level >= 4:
                instructions.append(
                    "• Keep details minimal and focused"
                    "\n• Include only essential information"
                )
            else:
                instructions.append(
                    "• Maintain balanced detail level"
                    "\n• Include important context without excess"
                )
                
            # Rapport Level Instructions (1=personal to 5=professional)
            rapport_level = self._last_calibrated_values['rapport_level']
            if rapport_level <= 2:
                instructions.append(
                    "• Maintain a warm, personal tone"
                    "\n• Show empathy and acknowledge personal context"
                )
            elif rapport_level >= 4:
                instructions.append(
                    "• Keep tone strictly professional"
                    "\n• Focus on facts and procedures"
                )
            else:
                instructions.append(
                    "• Balance professional and personal elements"
                    "\n• Show appropriate warmth while maintaining professionalism"
                )
            
            # Context Usage Instructions based on level
            instructions.append("\nContext Usage:")
            if level <= 30:
                instructions.append(
                    "• Reference context only for essential details"
                    "\n• Focus on standard procedures"
                    "\n• Maintain formal, protocol-based responses"
                )
            elif level <= 70:
                instructions.append(
                    "• Incorporate context naturally"
                    "\n• Balance personal details with procedures"
                    "\n• Adapt responses while maintaining focus"
                )
            else:
                instructions.append(
                    "• Fully utilize relevant context"
                    "\n• Personalize responses appropriately"
                    "\n• Maintain professional standards"
                )
            
            return "\n".join(instructions)
            
        except Exception as e:
            logger.error(f"Error generating style instructions: {str(e)}")
            return ""
    
    def get_case_file_display(self) -> str:
        """
        Generate a formatted string of calibrated values for the Case File viewer.
        """
        if not self._last_calibrated_values:
            return "**COMMUNICATION PARAMETERS**\nNo calibration data available"
            
        return (
            "**COMMUNICATION PARAMETERS**\n"
            f"Interaction Style: {self._last_calibrated_values['interaction_style']}\n"
            f"Detail Level: {self._last_calibrated_values['detail_level']}\n"
            f"Rapport Level: {self._last_calibrated_values['rapport_level']}\n"
            f"Differentiation Level: {self._differentiation_level}"
        )
    
    def apply_communication_controls(
        self,
        response: str,
        controls: Dict[str, Any]
    ) -> str:
        """
        Apply communication controls to response based on differentiation level.
        Respects user preferences while maintaining system stability.
        """
        try:
            # Generate style instructions first to update calibrated values
            style_instructions = self.generate_style_instructions(controls, self._differentiation_level)
            if style_instructions:
                logger.debug(f"Generated style instructions: {style_instructions}")
            
            modified_response = response
            
            # Apply name/title preferences if present
            name_prefs = controls.get('name_preference', {})
            if name_prefs:
                modified_response = self._apply_name_preferences(
                    modified_response,
                    name_prefs
                )
            
            # Apply demographic adaptations if present
            demographics = controls.get('demographics', {})
            if demographics:
                modified_response = self._apply_demographic_adaptations(
                    modified_response,
                    demographics
                )
            
            return modified_response
            
        except Exception as e:
            logger.error(f"Error applying communication controls: {str(e)}")
            return response
    
    def _apply_name_preferences(
        self,
        text: str,
        name_prefs: Dict[str, Any]
    ) -> str:
        """Apply name and title preferences."""
        try:
            preferred_name = name_prefs.get('preferred_name', '')
            if not preferred_name:
                return text
                
            # Apply professional title if required
            if name_prefs.get('title_required') and name_prefs.get('professional_title'):
                text = text.replace(
                    preferred_name,
                    f"{name_prefs['professional_title']} {preferred_name}"
                )
            
            return text
            
        except Exception as e:
            logger.error(f"Error applying name preferences: {str(e)}")
            return text
    
    def _apply_demographic_adaptations(
        self,
        text: str,
        demographics: Dict[str, Any]
    ) -> str:
        """Apply demographic-based adaptations."""
        try:
            age_cat = demographics.get('age_category', '').lower()
            prof_status = demographics.get('professional_status', '').lower()
            
            # Adapt for age category
            if age_cat == 'senior':
                text = self._enhance_clarity(text)
            elif age_cat == 'youth':
                text = self._simplify_language(text)
            
            # Adapt for professional status
            if prof_status == 'active':
                text = self._optimize_for_professional(text)
            elif prof_status == 'retired':
                text = self._enhance_detail(text)
            
            return text
            
        except Exception as e:
            logger.error(f"Error applying demographic adaptations: {str(e)}")
            return text
    
    def _enhance_clarity(self, text: str) -> str:
        """Enhance clarity for senior citizens."""
        # Add step numbers to lists
        # Break long sentences
        return text
    
    def _simplify_language(self, text: str) -> str:
        """Simplify language for youth."""
        # Use simpler terms
        # Add examples where helpful
        return text
    
    def _optimize_for_professional(self, text: str) -> str:
        """Optimize for busy professionals."""
        # Focus on key points
        # Add clear action items
        return text
    
    def _enhance_detail(self, text: str) -> str:
        """Enhance detail level."""
        # Add more context
        # Include additional explanations
        return text
