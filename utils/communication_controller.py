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
            
            # Core style parameters with descriptions
            instructions.append("Please adjust your communication style:")
            instructions.append(f"• Interaction Style: {self._last_calibrated_values['interaction_style']} ({'methodical' if self._last_calibrated_values['interaction_style'] <= 2 else 'efficient' if self._last_calibrated_values['interaction_style'] >= 4 else 'balanced'})")
            instructions.append(f"• Detail Level: {self._last_calibrated_values['detail_level']} ({'maximum' if self._last_calibrated_values['detail_level'] <= 2 else 'minimal' if self._last_calibrated_values['detail_level'] >= 4 else 'balanced'})")
            instructions.append(f"• Rapport Level: {self._last_calibrated_values['rapport_level']} ({'personal' if self._last_calibrated_values['rapport_level'] <= 2 else 'professional' if self._last_calibrated_values['rapport_level'] >= 4 else 'balanced'})")
            
            # Add behavioral guidance based on preferences
            instructions.append("\nBehavioral Guidance:")
            
            # Interaction Style
            if self._last_calibrated_values['interaction_style'] <= 2:
                instructions.extend([
                    "• Break down information into clear steps",
                    "• Provide structured, methodical guidance"
                ])
            elif self._last_calibrated_values['interaction_style'] >= 4:
                instructions.extend([
                    "• Communicate directly and efficiently",
                    "• Focus on key points and actions"
                ])
            
            # Detail Level
            if self._last_calibrated_values['detail_level'] <= 2:
                instructions.extend([
                    "• Include comprehensive explanations",
                    "• Provide relevant background information"
                ])
            elif self._last_calibrated_values['detail_level'] >= 4:
                instructions.extend([
                    "• Focus on essential information only",
                    "• Keep explanations brief and targeted"
                ])
            
            # Rapport Level
            if self._last_calibrated_values['rapport_level'] <= 2:
                instructions.extend([
                    "• Maintain a warm, personal approach",
                    "• Show empathy and understanding"
                ])
            elif self._last_calibrated_values['rapport_level'] >= 4:
                instructions.extend([
                    "• Keep tone formal and professional",
                    "• Focus on facts and procedures"
                ])
            
            # Add application guidance based on level
            if level <= 30:
                instructions.extend([
                    "\n>>> CONTEXT USAGE LEVEL: MINIMAL (0-30) <<<",
                    "APPLY PREFERENCES WITH MINIMAL ADHERENCE:",
                    "• Start with standardized RMV procedures as your base",
                    "• Consider the user's preferences shown above as minor adjustments only",
                    "• Keep responses primarily focused on standard protocol",
                    "• Use personal context only when directly relevant to procedures"
                ])
            elif level <= 70:
                instructions.extend([
                    "\n>>> CONTEXT USAGE LEVEL: MODERATE (31-70) <<<",
                    "APPLY PREFERENCES WITH MODERATE ADHERENCE:",
                    "• Balance standard RMV procedures with user's preferences",
                    "• Incorporate their preferred style while maintaining protocol",
                    "• Adapt responses while staying process-focused",
                    "• Use context to enhance understanding when appropriate"
                ])
            else:
                instructions.extend([
                    "\n>>> CONTEXT USAGE LEVEL: STRICT (71-100) <<<",
                    "APPLY PREFERENCES WITH STRICT ADHERENCE:",
                    "• Make user's preferred communication style your primary guide",
                    "• Fully embrace their preferences shown above",
                    "• Maintain professionalism while maximizing personalization",
                    "• Actively use context to enhance relevance"
                ])
            
            # Add formality and title preferences if above 50%
            if level > 50:
                if controls.get('title_required') and controls.get('professional_title'):
                    instructions.append(f"• Use title: {controls['professional_title']}")
                instructions.append(f"• Maintain {controls.get('formality_level', 'formal')} tone")
            
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
