"""
StyleCalibrator module for managing the balance between user preferences and system defaults.
Provides functionality to calibrate values based on a differentiation level.
"""

import logging
from typing import Union, Optional, Dict, Any
from enum import Enum, auto

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FormalityLevel(Enum):
    FORMAL = auto()
    SEMIFORMAL = auto()
    INFORMAL = auto()

class AgeCategory(Enum):
    SENIOR = auto()
    ADULT = auto()
    YOUTH = auto()

class ProfessionalStatus(Enum):
    ACTIVE = auto()
    RETIRED = auto()
    STUDENT = auto()
    NONE = auto()

class StyleCalibrator:
    """
    A utility class that calibrates style preferences between system defaults and user preferences.
    
    The calibration is controlled by a differentiation level that determines how strongly
    to apply user preferences versus system defaults.
    
    Attributes:
        differentiation_level (float): A value between 0 and 100 that determines the strength
            of user preferences. 0 means minimum values (1), 100 means maximum values (5).
    """
    
    # System defaults for structured variables
    SYSTEM_DEFAULTS = {
        'formality_level': 'formal',
        'title_required': False,
        'professional_title': '',
        'age_category': 'adult',
        'professional_status': 'none'
    }
    
    def __init__(self, differentiation_level: Union[int, float]) -> None:
        """
        Initialize the StyleCalibrator with a differentiation level.
        
        Args:
            differentiation_level: Value between 0-100 indicating how strongly to apply
                user preferences vs system defaults.
                
        Raises:
            ValueError: If differentiation_level is not between 0 and 100.
        """
        if not isinstance(differentiation_level, (int, float)):
            raise TypeError("differentiation_level must be a number")
        if not 0 <= differentiation_level <= 100:
            raise ValueError("differentiation_level must be between 0 and 100")
            
        self._differentiation_level = float(differentiation_level)
        logger.info(f"StyleCalibrator initialized with differentiation_level: {differentiation_level}")
        
    @property
    def differentiation_level(self) -> float:
        """Get the current differentiation level."""
        return self._differentiation_level

    def calibrate_structured_controls(
        self,
        controls: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calibrate structured communication controls based on differentiation level.
        
        Args:
            controls: Dictionary containing communication controls
            
        Returns:
            Dict[str, Any]: Calibrated communication controls
        """
        try:
            # Calculate the value on 1-5 scale based on differentiation level
            # At 0% -> 1.0
            # At 60% -> 3.0
            # At 100% -> 5.0
            scale_value = 1.0 + (self._differentiation_level / 100.0) * 4.0
            
            # Start with default controls
            calibrated = self.SYSTEM_DEFAULTS.copy()
            
            # Set numeric values based on scale
            calibrated['interaction_style'] = round(scale_value, 1)
            calibrated['detail_level'] = round(scale_value, 1)
            calibrated['rapport_level'] = round(scale_value, 1)
            
            # Extract name preferences and demographics
            name_prefs = controls.get('name_preference', {})
            demographics = controls.get('demographics', {})
            
            # Calibrate formality level
            if self._differentiation_level > 50:  # Above 50% differentiation, use user's formality
                calibrated['formality_level'] = name_prefs.get('formality_level', self.SYSTEM_DEFAULTS['formality_level'])
            
            # Calibrate title usage
            if self._differentiation_level > 25:  # Above 25% differentiation, respect title requirements
                calibrated['title_required'] = name_prefs.get('title_required', self.SYSTEM_DEFAULTS['title_required'])
                calibrated['professional_title'] = name_prefs.get('professional_title', self.SYSTEM_DEFAULTS['professional_title'])
            
            # Calibrate demographics
            if self._differentiation_level > 30:  # Above 30% differentiation, use demographic preferences
                calibrated['age_category'] = demographics.get('age_category', self.SYSTEM_DEFAULTS['age_category'])
                calibrated['professional_status'] = demographics.get('professional_status', self.SYSTEM_DEFAULTS['professional_status'])
            
            return calibrated
            
        except Exception as e:
            logger.error(f"Error calibrating structured controls: {str(e)}")
            return self.SYSTEM_DEFAULTS
        
    def calibrate(
        self, 
        user_preference: Union[int, float], 
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> float:
        """
        Calibrate a value between minimum (1) and maximum (5) based on differentiation level.
        
        Args:
            user_preference: The user's preferred value
            min_value: Optional minimum allowed value
            max_value: Optional maximum allowed value
            
        Returns:
            float: The calibrated value
            
        Raises:
            TypeError: If user_preference is not a number
            ValueError: If min_value is greater than max_value
        """
        if not isinstance(user_preference, (int, float)):
            raise TypeError("user_preference must be a number")
            
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError("min_value cannot be greater than max_value")
        
        # Calculate value on 1-5 scale
        calibrated = 1.0 + (self._differentiation_level / 100.0) * 4.0
        
        # Apply bounds if provided
        if min_value is not None:
            calibrated = max(calibrated, min_value)
        if max_value is not None:
            calibrated = min(calibrated, max_value)
            
        logger.debug(f"Calibrated value: {calibrated} (differentiation_level: {self._differentiation_level})")
        
        return round(calibrated, 1)
