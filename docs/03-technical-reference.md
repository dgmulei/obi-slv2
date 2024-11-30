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

### Case File Display Updates

```python
def display_case_file(content1: Optional[str], content2: Optional[str]) -> None:
    # Real-time updates based on context changes
    if context.needs_refresh:
        content = get_case_file_content(context, conversation_manager)
        context.needs_refresh = False
```

### Dynamic Context Intelligence

```python
# Store latest calibration as assistant message
self.latest_calibration_message = {
    "role": "assistant",
    "content": (
        "[COMMUNICATION UPDATE] Please adjust your communication style:\n"
        f"- Interaction Style: {calibrated_controls['interaction_style']}\n"
        f"- Detail Level: {calibrated_controls['detail_level']}\n"
        f"- Rapport Level: {calibrated_controls['rapport_level']}"
    )
}

# Include calibration in message flow
messages = []
if self.latest_calibration_message:
    messages.append(self.latest_calibration_message)
messages.append({
    "role": "user",
    "content": message
})
```

### Style Calibration Impact

```python
def update_differentiation_level(self, value: float):
    self._differentiation_level = value
    # Update all active enhanced managers
    for thread_id, enhanced_manager in self.session_manager.enhanced_managers.items():
        enhanced_manager.update_differentiation_level(value)
        self.session_manager.active_sessions[thread_id].needs_refresh = True
```

### Message Flow Architecture

The system implements a sophisticated message flow that combines:
1. Base System Context: Provided through system prompt
2. Dynamic Calibration: Delivered through in-conversation messages
3. User Interaction: Maintained through message history

Key aspects:
- Calibration updates are sent as assistant messages
- Each user message includes the latest calibration context
- System prompt includes instruction to handle [COMMUNICATION UPDATE] messages
- Only the most recent calibration is maintained and used

### Claude API Integration

The system integrates with Claude's Messages API following these principles:
1. System-level instructions via top-level system parameter
2. Dynamic updates via in-conversation assistant messages
3. Clear message role separation (system vs assistant vs user)
4. Explicit update markers for clear instruction handling

### System Components

#### EnhancedConversationManager
- Manages conversation flow and context
- Handles Claude API interactions
- Maintains calibration state
- Processes user messages

#### StyleCalibrator
- Converts slider values (0-100) to calibrated controls
- Maintains differentiation levels
- Provides structured communication instructions

#### ConversationManager
- Coordinates multiple conversations
- Manages user profiles
- Handles session initialization
- Coordinates with storage system

### Data Flow

#### Message Processing
1. User sends message
2. Latest calibration included
3. System prompt provides base context
4. Claude processes complete context
5. Response maintains calibrated style

#### Context Updates
1. Slider adjustment triggers update
2. New calibration message created
3. Stored as latest calibration
4. Applied to next message
5. Previous calibrations superseded

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

### Error Handling

#### API Errors
- Model overload handling
- Fallback model implementation
- Error logging and tracking
- Graceful degradation

#### System Errors
- Exception handling
- Error logging
- User feedback
- Recovery procedures

### Performance Optimization

#### Message Efficiency
- Minimal message payload
- Efficient calibration updates
- Optimized message flow
- Response caching when appropriate

#### System Resources
- Memory management
- API call optimization
- Storage efficiency
- Processing optimization

### Monitoring and Logging

#### System Logs
- API interaction logging
- Error tracking
- Performance monitoring
- Usage statistics

#### User Interaction
- Message success rates
- Response times
- Calibration effectiveness
- User engagement metrics

### Development Guidelines

#### Code Standards
- Clear documentation
- Consistent formatting
- Error handling
- Type annotations

#### Testing Requirements
- Unit test coverage
- Integration testing
- API interaction tests
- Error condition testing

### Deployment Considerations

#### Environment Setup
- API key configuration
- Storage setup
- Security implementation
- Monitoring configuration

#### Maintenance
- Regular updates
- Performance monitoring
- Security patches
- System backups

### Future Enhancements

#### Planned Features
- Enhanced analytics
- Additional integrations
- Performance improvements
- Extended functionality

#### Optimization Areas
- Response time
- Memory usage
- Storage efficiency
- API utilization
