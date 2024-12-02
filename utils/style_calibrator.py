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
        Level 0-30: Mostly system defaults
        Level 31-70: Blend preferences
        Level 71-100: Full user preferences
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
        """
        if not self._last_calibrated_values:
            return "**COMMUNICATION PARAMETERS**\nNo calibration data available"
            
        return (
            "**COMMUNICATION PARAMETERS**\n"
            f"Interaction Style: {self._last_calibrated_values['interaction_style']}\n"
            f"Detail Level: {self._last_calibrated_values['detail_level']}\n"
            f"Rapport Level: {self._last_calibrated_values['rapport_level']}\n"
            f"Current Level: {self._differentiation_level}"
        )

    def _calculate_preference_weight(self) -> float:
        """
        Calculate weight for user preferences based on differentiation level.
        0-30: Very low weight (0.0 to 0.2)
        31-70: Medium weight (0.2 to 0.8)
        71-100: High weight (0.8 to 1.0)
        """
        level = self._differentiation_level
        
        if level <= 30:
            # Linear scale from 0.0 to 0.2
            return (level / 30) * 0.2
        elif level <= 70:
            # Linear scale from 0.2 to 0.8
            return 0.2 + ((level - 30) / 40) * 0.6
        else:
            # Linear scale from 0.8 to 1.0
            return 0.8 + ((level - 70) / 30) * 0.2

    def _generate_behavioral_instructions(self, controls: Dict[str, Any]) -> str:
        """Generate behavioral instructions based on differentiation level and controls."""
        level = self._differentiation_level
        
        # Base instructions that apply at all levels
        instructions = [
            "Please adjust your communication style:",
            f"• Interaction Style: {controls['interaction_style']}",
            f"• Detail Level: {controls['detail_level']}",
            f"• Rapport Level: {controls['rapport_level']}"
        ]
        
        # Add level-specific behavioral guidance
        if level <= 30:
            instructions.extend([
                "",
                "Context Usage:",
                "• Maintain awareness of complete context",
                "• Focus on protocol-based responses",
                "• Use formal, standardized language",
                "• Reference personal details only when directly relevant to procedures",
                "• Prioritize clear procedural guidance"
            ])
        elif level <= 70:
            instructions.extend([
                "",
                "Context Usage:",
                "• Incorporate context naturally in responses",
                "• Balance protocol with personalization",
                "• Adapt language to user preferences",
                "• Include relevant personal details to support understanding",
                "• Maintain professional focus while showing awareness of user situation"
            ])
        else:
            instructions.extend([
                "",
                "Context Usage:",
                "• Fully utilize all relevant context",
                "• Prioritize user's documented preferences",
                "• Match communication style precisely",
                "• Incorporate personal details to enhance relevance",
                "• Maintain professional standards while maximizing personalization"
            ])
        
        # Add formality and title preferences if above 50%
        if level > 50:
            if controls.get('title_required') and controls.get('professional_title'):
                instructions.append(f"• Use title: {controls['professional_title']}")
            instructions.append(f"• Maintain {controls.get('formality_level', 'formal')} tone")
        
        return "\n".join(instructions)

    def calibrate_structured_controls(
        self,
        user_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calibrate communication controls based on differentiation level.
        Respects user preferences while maintaining system stability.
        """
        try:
            # Calculate preference weight
            weight = self._calculate_preference_weight()
            logger.debug(f"Calculated preference weight: {weight}")
            
            # Start with system defaults
            calibrated = self.SYSTEM_DEFAULTS.copy()
            
            # Get communication preferences
            comm_prefs = user_preferences.get('communication_preferences', {})
            
            # Calibrate core communication styles
            core_values = {}
            for key in ['interaction_style', 'detail_level', 'rapport_level']:
                user_value = comm_prefs.get(key, self.SYSTEM_DEFAULTS[key])
                # Weighted average between system default and user preference
                calibrated[key] = round(
                    self.SYSTEM_DEFAULTS[key] * (1 - weight) + 
                    user_value * weight,
                    1
                )
                core_values[key] = calibrated[key]
            
            # Store calibrated values for Case File display
            self._last_calibrated_values = core_values
            
            # Always include additional preferences but apply them based on weight
            name_prefs = user_preferences.get('name_preference', {})
            demographics = user_preferences.get('demographics', {})
            
            calibrated['formality_level'] = name_prefs.get('formality_level', self.SYSTEM_DEFAULTS['formality_level'])
            calibrated['title_required'] = name_prefs.get('title_required', self.SYSTEM_DEFAULTS['title_required'])
            calibrated['professional_title'] = name_prefs.get('professional_title', self.SYSTEM_DEFAULTS['professional_title'])
            calibrated['age_category'] = demographics.get('age_category', self.SYSTEM_DEFAULTS['age_category'])
            calibrated['professional_status'] = demographics.get('professional_status', self.SYSTEM_DEFAULTS['professional_status'])
            
            logger.debug(f"Calibrated controls: {calibrated}")
            return calibrated
            
        except Exception as e:
            logger.error(f"Error calibrating structured controls: {str(e)}")
            self._last_calibrated_values = None
            return self.SYSTEM_DEFAULTS.copy()

    def calibrate(
        self, 
        user_preference: Union[int, float]
    ) -> float:
        """
        Calibrate a single value between system default and user preference.
        Respects the user's preferred value based on differentiation level.
        """
        if not isinstance(user_preference, (int, float)):
            raise TypeError("user_preference must be a number")
        
        # Calculate weight for user preference
        weight = self._calculate_preference_weight()
        
        # Weighted average between system default and user preference
        calibrated = self.SYSTEM_DEFAULTS['interaction_style'] * (1 - weight) + user_preference * weight
        
        return round(calibrated, 1)

    def generate_style_instructions(self, controls: Dict[str, Any]) -> str:
        """Generate style instructions based on current calibration."""
        return self._generate_behavioral_instructions(controls)
