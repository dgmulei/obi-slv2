# Obi Technical Reference

## Core Components

### StyleCalibrator
```python
class StyleCalibrator:
    """
    Preserves user's raw communication preferences (1-5 scale).
    No value blending - preferences stay pure at all differentiation levels.
    """
    def calibrate_structured_controls(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        # Get communication preferences
        comm_prefs = user_preferences.get('communication_preferences', {})
        
        # Use raw values (1-5 scale)
        return {
            'interaction_style': comm_prefs.get('interaction_style', 3),  # methodical (1) to efficient (5)
            'detail_level': comm_prefs.get('detail_level', 3),      # maximum (1) to minimal (5)
            'rapport_level': comm_prefs.get('rapport_level', 3)     # personal (1) to professional (5)
        }
```

### CommunicationController
```python
class CommunicationController:
    """
    Formats [COMMUNICATION UPDATE] messages with three parts:
    1. Raw preferences (preserved)
    2. Behavioral guidance (matches preferences)
    3. Application guidance (varies with level)
    """
    def generate_style_instructions(self, controls: Dict[str, Any], level: float) -> str:
        instructions = []
        
        # 1. Raw Preferences
        instructions.append("Please adjust your communication style:")
        instructions.append(f"• Interaction Style: {controls['interaction_style']} ({'efficient' if controls['interaction_style'] >= 4 else 'methodical' if controls['interaction_style'] <= 2 else 'balanced'})")
        instructions.append(f"• Detail Level: {controls['detail_level']} ({'minimal' if controls['detail_level'] >= 4 else 'maximum' if controls['detail_level'] <= 2 else 'balanced'})")
        instructions.append(f"• Rapport Level: {controls['rapport_level']} ({'professional' if controls['rapport_level'] >= 4 else 'personal' if controls['rapport_level'] <= 2 else 'balanced'})")
        
        # 2. Behavioral Guidance (matches preferences)
        instructions.append("\nBehavioral Guidance:")
        if controls['interaction_style'] >= 4:
            instructions.extend([
                "• Communicate directly and efficiently",
                "• Focus on key points and actions"
            ])
        elif controls['interaction_style'] <= 2:
            instructions.extend([
                "• Break down information into clear steps",
                "• Provide structured, methodical guidance"
            ])
            
        if controls['detail_level'] >= 4:
            instructions.extend([
                "• Focus on essential information only",
                "• Keep explanations brief and targeted"
            ])
        elif controls['detail_level'] <= 2:
            instructions.extend([
                "• Include comprehensive explanations",
                "• Provide relevant background information"
            ])
            
        if controls['rapport_level'] >= 4:
            instructions.extend([
                "• Keep tone formal and professional",
                "• Focus on facts and procedures"
            ])
        elif controls['rapport_level'] <= 2:
            instructions.extend([
                "• Maintain a warm, personal approach",
                "• Show empathy and understanding"
            ])
        
        # 3. Application Guidance (varies with level)
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
        
        return "\n".join(instructions)
```

### EnhancedConversationManager
```python
class EnhancedConversationManager:
    """
    Manages message flow and context display.
    Preserves preferences while controlling their application.
    """
    def _get_communication_preferences(self) -> Dict[str, Any]:
        """Get communication preferences in the correct structure."""
        if not self.user_profile:
            return {}
            
        # Get preferences from metadata
        preferences = self.user_profile.get('metadata', {}).get('communication_preferences', {})
        
        # Create properly structured dict
        return {
            'communication_preferences': preferences
        }

    def update_differentiation_level(self, value: float) -> None:
        """Update differentiation level and recalibrate."""
        try:
            # Get preferences in correct structure
            preferences = self._get_communication_preferences()
            
            # Get calibrated controls (raw preferences)
            calibrated_controls = self.style_calibrator.calibrate_structured_controls(preferences)
            
            # Generate behavioral instructions
            style_instructions = self.communication_controller.generate_style_instructions(
                calibrated_controls,
                value  # differentiation_level controls application
            )
            
            # Create calibration message
            self.latest_calibration_message = {
                "role": "assistant",
                "content": f"[COMMUNICATION UPDATE] {style_instructions}"
            }
            
            # Update project folder
            self.current_project_folder = ProjectFolder(
                user_profile=self.user_profile,
                system_prompt=self.system_prompt,
                calibrated_controls=calibrated_controls,
                latest_calibration_message=self.latest_calibration_message
            )
            
        except Exception as e:
            logger.error(f"Error updating differentiation level: {str(e)}")
            raise
```

### Case File Display
```python
def get_case_file_content(context: ConversationContext, conversation_manager: ConversationManager) -> Optional[str]:
    """
    Shows both formatted summary and complete context.
    """
    try:
        if not context.active_user_profile:
            return None
            
        enhanced_manager = conversation_manager.session_manager.enhanced_managers.get(context.thread_id)
        if not enhanced_manager or not enhanced_manager.current_project_folder:
            return None
            
        sections = []
        
        # 1. Formatted Summary (user-friendly)
        sections.append("=== FORMATTED SUMMARY ===")
        sections.append(enhanced_manager.current_project_folder.get_context_summary())
        
        # 2. Claude's Context (complete system view)
        sections.append("\n=== CLAUDE'S CONTEXT ===")
        sections.append("# System Instructions")
        sections.append(enhanced_manager.system_prompt)
        sections.append("\n# User Profile")
        sections.append(str(context.active_user_profile))
        sections.append("\n# Communication Parameters")
        sections.append(str(enhanced_manager.latest_calibration_message))
        
        # Join sections and wrap in code block
        sections_text = '\n'.join(sections)
        return f"```text\n{sections_text}\n```"
        
    except Exception as e:
        logger.error(f"Error getting case file content: {str(e)}")
        return None
```

## Message Flow

### [COMMUNICATION UPDATE] Structure

The system uses a consistent three-part message structure:

1. Raw Preferences (always preserved)
   ```
   Please adjust your communication style:
   • Interaction Style: 5 (efficient)
   • Detail Level: 5 (minimal)
   • Rapport Level: 5 (professional)
   ```

2. Behavioral Guidance (matches preferences)
   ```
   Behavioral Guidance:
   • Communicate directly and efficiently
   • Focus on key points and actions
   • Focus on essential information only
   • Keep explanations brief and targeted
   • Keep tone strictly professional
   • Focus on facts and procedures
   ```

3. Application Guidance (varies with level)
   ```
   At level 0:
   >>> CONTEXT USAGE LEVEL: MINIMAL (0-30) <<<
   APPLY PREFERENCES WITH MINIMAL ADHERENCE:
   • Start with standardized procedures
   • Consider preferences as minor adjustments
   • Keep responses protocol-focused

   At level 50:
   >>> CONTEXT USAGE LEVEL: MODERATE (31-70) <<<
   APPLY PREFERENCES WITH MODERATE ADHERENCE:
   • Balance procedures with preferences
   • Incorporate preferred style while maintaining protocol
   • Adapt responses while staying process-focused

   At level 100:
   >>> CONTEXT USAGE LEVEL: STRICT (71-100) <<<
   APPLY PREFERENCES WITH STRICT ADHERENCE:
   • Make preferences primary guide
   • Fully embrace preferred style
   • Maximize personalization while professional
   ```

### Case File Organization

The display shows both user-friendly summary and complete system context:

1. FORMATTED SUMMARY
   - Critical License Information
   - Documentation Status
   - Payment Information
   - Personal Information
   - Latest Communication Update showing:
     * User preferences (1-5)
     * Behavioral guidance
     * Application level

2. CLAUDE'S CONTEXT
   - Complete system instructions
   - Raw user profile data
   - Communication parameters including:
     * Current preference values
     * Latest [COMMUNICATION UPDATE]
     * Application guidance

## Error Handling

### Enhanced Error Handling
```python
def get_response(self, message: str) -> str:
    try:
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=messages,
            system=self.system_prompt,
            max_tokens=1024,
            temperature=0.7
        )
    except Exception as e:
        if "overloaded_error" in str(e):
            logger.warning("Claude 3 Sonnet is overloaded, falling back to Claude 3 Opus")
            response = self.anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                messages=messages,
                system=self.system_prompt,
                max_tokens=1024,
                temperature=0.7
            )
```

## Development Guidelines

### Code Standards
- Clear documentation
- Consistent formatting
- Error handling
- Type annotations
- Context validation
- Profile validation

### Testing Requirements
- Unit test coverage
- Integration testing
- API interaction tests
- Error condition testing
- Context persistence tests
- Profile validation tests

## Deployment Considerations

### Environment Setup
- API key configuration
- Storage setup
- Security implementation
- Monitoring configuration
- Cache configuration
- Profile storage setup

### Maintenance
- Regular updates
- Performance monitoring
- Security patches
- System backups
- Cache maintenance
- Profile data cleanup
