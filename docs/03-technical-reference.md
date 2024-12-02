# Obi - Massachusetts RMV Service Agent Technical Documentation

## Core Architecture

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

### Context Intelligence Scaling

```python
class StyleCalibrator:
    def calibrate_controls(self, differentiation_level: float) -> Dict[str, float]:
        # Level 0 Behavior (Pure System)
        if differentiation_level == 0:
            return {
                "interaction_style": self.system_defaults["interaction_style"],
                "detail_level": self.system_defaults["detail_level"],
                "rapport_level": self.system_defaults["rapport_level"]
            }
        
        # Linear scaling from system defaults to user preferences
        weight = min(1.0, differentiation_level / 100.0)
        
        # Feature thresholds
        if weight < 0.3:
            # Minimal personalization
            weight *= 0.5
        elif weight < 0.5:
            # Moderate personalization
            weight *= 0.75
            
        return {
            "interaction_style": self._calculate_weighted_value("interaction_style", weight),
            "detail_level": self._calculate_weighted_value("detail_level", weight),
            "rapport_level": self._calculate_weighted_value("rapport_level", weight)
        }
```

### Enhanced Context Management

```python
@dataclass
class ProjectFolder:
    """Represents the comprehensive context for a user session."""
    user_profile: Dict[str, Any]
    system_prompt: str
    calibrated_controls: Dict[str, Any]

    def get_context_summary(self) -> str:
        """Get formatted summary of user context with prioritized information."""
        profile = self.user_profile
        summary = []

        # Critical License Information first
        if license_info := profile.get('license', {}).get('current', {}):
            summary.append("=== CRITICAL LICENSE INFORMATION ===")
            if type_ := license_info.get('type'):
                summary.append(f"Type: {type_}")
            if expiration := license_info.get('expiration'):
                summary.append(f"EXPIRATION: {expiration}")
            if restrictions := license_info.get('restrictions', []):
                summary.append(f"RESTRICTIONS: {', '.join(restrictions)}")

        # Documentation Status
        if docs := profile.get('documentation', {}):
            summary.append("=== DOCUMENTATION STATUS ===")
            for doc_type, doc_info in docs.items():
                if isinstance(doc_info, dict):
                    status = doc_info.get('status', 'Unknown')
                    expiry = doc_info.get('expiration', 'Not specified')
                    summary.append(f"{doc_type}: {status} (Expires: {expiry})")

        return "\n".join(summary)
```

### Profile Management

```python
class PersonalInfo(TypedDict, total=False):
    full_name: str
    primary_language: str
    email: Optional[str]
    phone: Optional[str]
    dob: Optional[str]  # Optional date of birth

class UserProfile(TypedDict):
    personal: PersonalInfo
    addresses: Dict[str, AddressInfo]
    license: LicenseInfo
    documentation: Dict[str, Any]
    additional: Dict[str, Any]
    health: Dict[str, Any]
    payment: Dict[str, Any]
    metadata: Dict[str, Any]
    communication_preferences: CommunicationPreferences
```

### Message Flow Architecture

The system implements a sophisticated message flow that combines:
1. Base System Context: Provided through system prompt
2. Dynamic Calibration: Delivered through in-conversation messages
3. User Interaction: Maintained through message history
4. Context Markers: Track numbered lists, reference points, and key details

Key aspects:
- Calibration updates are sent as assistant messages
- Each user message includes the latest calibration context
- System prompt includes instruction to handle [COMMUNICATION UPDATE] messages
- Only the most recent calibration is maintained and used
- Conversation context is preserved across all intelligence levels
- Profile data is cached with TTL for consistent access

### Case File Display Architecture

The Case File display is organized into clear sections:

1. System Instructions
   - Raw system rules/parameters sent to Claude
   - Core service parameters
   - Base context information

2. User Profile
   - Complete YAML profile
   - Metadata and descriptions
   - Static profile data

3. Communication Parameters
   - Current numerical values
   - Active instructions
   - Real-time calibration state

4. Active Alerts
   - Violations
   - Restrictions
   - Payment issues
   - Critical notifications

5. Support System
   - Emergency contacts
   - Previous assistance history
   - Professional status
   - Support network details

6. Behavioral Guidance
   - Differentiation level
   - Style instructions
   - Context usage parameters
   - Current calibration state

7. System State
   - Context awareness level
   - Active memory status
   - Current calibration
   - Debug information

### Claude API Integration

The system integrates with Claude's Messages API following these principles:
1. System-level instructions via top-level system parameter
2. Dynamic updates via in-conversation assistant messages
3. Clear message role separation (system vs assistant vs user)
4. Explicit update markers for clear instruction handling
5. Context validation before each response
6. Automatic fallback to Claude-3-Opus when Sonnet is overloaded

### System Components

#### EnhancedConversationManager
- Manages conversation flow and context
- Handles Claude API interactions with fallback mechanism
- Maintains calibration state
- Processes user messages
- Implements conversation memory
- Validates context completeness
- Manages ProjectFolder for comprehensive session context

#### StyleCalibrator
- Converts slider values (0-100) to calibrated controls
- Maintains differentiation levels
- Provides structured communication instructions
- Implements linear scaling with thresholds
- Ensures clean separation between system and user preferences

#### ConversationManager
- Coordinates multiple conversations
- Manages user profiles with TTL caching
- Handles session initialization
- Coordinates with storage system
- Maintains conversation markers
- Implements profile validation

### Data Flow

#### Message Processing
1. User sends message
2. Context validation performed
3. Latest calibration included
4. System prompt provides base context
5. Conversation markers updated
6. Claude processes complete context
7. Response maintains calibrated style
8. Fallback handling if needed

#### Context Updates
1. Slider adjustment triggers update
2. New calibration message created
3. Stored as latest calibration
4. Applied to next message
5. Previous calibrations superseded
6. Context markers preserved

### Security Considerations

#### API Security
- Secure API key handling
- Rate limiting implementation
- Error handling and fallbacks
- Secure message processing

#### Data Protection
- User profile security
- Message encryption
- Secure storage handling
- Access control implementation
- Profile data validation
- Cached data TTL enforcement

### Error Handling

#### API Errors
- Model overload handling with automatic fallback
- Fallback model implementation (Claude-3-Opus)
- Error logging and tracking
- Graceful degradation

#### System Errors
- Exception handling
- Error logging
- User feedback
- Recovery procedures
- Profile validation errors
- Context validation failures

### Performance Optimization

#### Message Efficiency
- Minimal message payload
- Efficient calibration updates
- Optimized message flow
- Response caching when appropriate
- Profile data caching
- Context marker optimization

#### System Resources
- Memory management
- API call optimization
- Storage efficiency
- Processing optimization
- Cache TTL management
- Context validation efficiency

### Monitoring and Logging

#### System Logs
- API interaction logging
- Error tracking
- Performance monitoring
- Usage statistics
- Profile validation results
- Context validation status

#### User Interaction
- Message success rates
- Response times
- Calibration effectiveness
- User engagement metrics
- Context persistence metrics
- Profile access patterns

### Development Guidelines

#### Code Standards
- Clear documentation
- Consistent formatting
- Error handling
- Type annotations
- Context validation
- Profile validation

#### Testing Requirements
- Unit test coverage
- Integration testing
- API interaction tests
- Error condition testing
- Context persistence tests
- Profile validation tests

### Deployment Considerations

#### Environment Setup
- API key configuration
- Storage setup
- Security implementation
- Monitoring configuration
- Cache configuration
- Profile storage setup

#### Maintenance
- Regular updates
- Performance monitoring
- Security patches
- System backups
- Cache maintenance
- Profile data cleanup

### Future Enhancements

#### Planned Features
- Enhanced analytics
- Additional integrations
- Performance improvements
- Extended functionality
- Advanced context tracking
- Profile optimization

#### Optimization Areas
- Response time
- Memory usage
- Storage efficiency
- API utilization
- Context persistence
- Profile caching
