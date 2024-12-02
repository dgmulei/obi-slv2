"""
StyleCalibrator module for managing the balance between user preferences and system defaults.
"""

import logging
from typing import Union, Dict, Any, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StyleCalibrator:
    """
    Calibrates style preferences between system defaults and user preferences.
    At level 0-30: Mostly standardized responses regardless of preferences
    At level 31-70: Begin incorporating user preferences
    At level 71-100: Strictly adhere to documented preferences
    """
    
    # System defaults - balanced middle ground
    SYSTEM_DEFAULTS = {
        'interaction_style': 3,  # Balanced between methodical (1) and efficient (5)
        'detail_level': 3,      # Balanced between maximum (1) and minimal (5)
        'rapport_level': 3,     # Balanced between personal (1) and professional (5)
        'formality_level': 'formal',
        'title_required': False,
        'professional_title': '',
        'age_category': 'adult',
        'professional_status': 'none'
    }
    
    def __init__(self, differentiation_level: Union[int, float]) -> None:
        """
        Initialize with differentiation level (0-100).
        Level 0-30: Mostly standardized responses
        Level 31-70: Begin incorporating preferences
        Level 71-100: Strictly adhere to preferences
        """
        if not isinstance(differentiation_level, (int, float)):
            raise TypeError("differentiation_level must be a number")
        if not 0 <= differentiation_level <= 100:
            raise ValueError("differentiation_level must be between 0 and 100")
            
        self._differentiation_level = float(differentiation_level)
        self._last_calibrated_values = None
        logger.info(f"StyleCalibrator initialized with differentiation_level: {differentiation_level}")

    @property
    def differentiation_level(self) -> float:
        """Get the current differentiation level."""
        return self._differentiation_level

    @property
    def last_calibrated_values(self) -> Dict[str, float]:
        """Get the most recently calibrated communication parameter values."""
        return self._last_calibrated_values or {}

    def get_case_file_display(self) -> str:
        """
        Generate a formatted string of calibrated values for the Case File viewer.
        Shows raw preferences and current application level.
        """
        if not self._last_calibrated_values:
            return "**COMMUNICATION PARAMETERS**\nNo calibration data available"
            
        # Determine application level description
        level_desc = (
            "Minimal" if self._differentiation_level <= 30 else
            "Moderate" if self._differentiation_level <= 70 else
            "Strict"
        )
            
        return (
            "**COMMUNICATION PARAMETERS**\n"
            f"Interaction Style: {self._last_calibrated_values['interaction_style']}\n"
            f"Detail Level: {self._last_calibrated_values['detail_level']}\n"
            f"Rapport Level: {self._last_calibrated_values['rapport_level']}\n"
            f"Application Level: {level_desc} ({self._differentiation_level})"
        )

    def calibrate_structured_controls(
        self,
        user_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get user's raw preferences and determine application strength.
        No more value blending - preferences stay pure.
        """
        try:
            # Log incoming preferences
            logger.info(f"Calibrating controls with preferences: {user_preferences}")
            
            # Get communication preferences
            comm_prefs = user_preferences.get('communication_preferences', {})
            logger.info(f"Found communication preferences: {comm_prefs}")
            
            # Use raw preferences (no blending)
            calibrated = {}
            for key in ['interaction_style', 'detail_level', 'rapport_level']:
                if key not in comm_prefs:
                    logger.warning(f"No {key} found in preferences, using default: {self.SYSTEM_DEFAULTS[key]}")
                    calibrated[key] = self.SYSTEM_DEFAULTS[key]
                else:
                    logger.info(f"Using preference value for {key}: {comm_prefs[key]}")
                    calibrated[key] = comm_prefs[key]
            
            # Store raw values for Case File display
            self._last_calibrated_values = calibrated.copy()
            logger.info(f"Final calibrated values: {calibrated}")
            
            # Add name/demographic preferences unchanged
            name_prefs = user_preferences.get('name_preference', {})
            demographics = user_preferences.get('demographics', {})
            
            calibrated['formality_level'] = name_prefs.get('formality_level', self.SYSTEM_DEFAULTS['formality_level'])
            calibrated['title_required'] = name_prefs.get('title_required', self.SYSTEM_DEFAULTS['title_required'])
            calibrated['professional_title'] = name_prefs.get('professional_title', self.SYSTEM_DEFAULTS['professional_title'])
            calibrated['age_category'] = demographics.get('age_category', self.SYSTEM_DEFAULTS['age_category'])
            calibrated['professional_status'] = demographics.get('professional_status', self.SYSTEM_DEFAULTS['professional_status'])
            
            return calibrated
            
        except Exception as e:
            logger.error(f"Error calibrating structured controls: {str(e)}")
            self._last_calibrated_values = None
            return self.SYSTEM_DEFAULTS.copy()

    def generate_style_instructions(self, controls: Dict[str, Any]) -> str:
        """Generate style instructions based on current calibration."""
        return self._generate_behavioral_instructions(controls)

    def _generate_behavioral_instructions(self, controls: Dict[str, Any]) -> str:
        """Generate behavioral instructions based on differentiation level and controls."""
        level = self._differentiation_level
        
        # Log the controls being used for instructions
        logger.info(f"Generating instructions with controls: {controls}")
        
        # Determine application level description
        level_desc = (
            "minimal" if level <= 30 else
            "moderate" if level <= 70 else
            "strict"
        )
        
        # Base instructions showing raw preferences
        instructions = [
            "Please adjust your communication style:",
            f"• Interaction Style: {controls['interaction_style']} ({'methodical' if controls['interaction_style'] <= 2 else 'efficient' if controls['interaction_style'] >= 4 else 'balanced'})",
            f"• Detail Level: {controls['detail_level']} ({'maximum' if controls['detail_level'] <= 2 else 'minimal' if controls['detail_level'] >= 4 else 'balanced'})",
            f"• Rapport Level: {controls['rapport_level']} ({'personal' if controls['rapport_level'] <= 2 else 'professional' if controls['rapport_level'] >= 4 else 'balanced'})",
            "",
            f"Apply these preferences with {level_desc} adherence ({level:.0f}% differentiation level)."
        ]
        
        # Add behavioral guidance based on raw preferences
        instructions.append("\nBehavioral Guidance:")
        
        # Interaction Style
        if controls['interaction_style'] <= 2:
            instructions.extend([
                "• Break down information into clear steps",
                "• Provide structured, methodical guidance"
            ])
        elif controls['interaction_style'] >= 4:
            instructions.extend([
                "• Communicate directly and efficiently",
                "• Focus on key points and actions"
            ])
        
        # Detail Level
        if controls['detail_level'] <= 2:
            instructions.extend([
                "• Include comprehensive explanations",
                "• Provide relevant background information"
            ])
        elif controls['detail_level'] >= 4:
            instructions.extend([
                "• Focus on essential information only",
                "• Keep explanations brief and targeted"
            ])
        
        # Rapport Level
        if controls['rapport_level'] <= 2:
            instructions.extend([
                "• Maintain a warm, personal approach",
                "• Show empathy and understanding"
            ])
        elif controls['rapport_level'] >= 4:
            instructions.extend([
                "• Keep tone formal and professional",
                "• Focus on facts and procedures"
            ])
        
        # Add application guidance based on level
        instructions.append("\nApplication Guidance:")
        if level <= 30:
            instructions.extend([
                "• Default to standardized responses and procedures",
                "• Consider preferences as minor adjustments only",
                "• Keep responses primarily protocol-focused",
                "• Use personal context only when directly relevant"
            ])
        elif level <= 70:
            instructions.extend([
                "• Balance standard procedures with preferences",
                "• Incorporate preferences while maintaining protocol",
                "• Adapt responses while staying process-focused",
                "• Use context to enhance understanding when appropriate"
            ])
        else:
            instructions.extend([
                "• Make user preferences your primary guide",
                "• Fully embrace the preferred communication style",
                "• Maintain professionalism while maximizing personalization",
                "• Actively use context to enhance relevance"
            ])
        
        # Add formality and title preferences if above 50%
        if level > 50:
            if controls.get('title_required') and controls.get('professional_title'):
                instructions.append(f"• Use title: {controls['professional_title']}")
            instructions.append(f"• Maintain {controls.get('formality_level', 'formal')} tone")
        
        return "\n".join(instructions)
