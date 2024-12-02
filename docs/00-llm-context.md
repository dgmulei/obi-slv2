# LLM Context Guide

⚠️ CRITICAL: This document is designed specifically for LLMs. READ THIS FIRST before making any changes to the system.

## STOP AND THINK

Before ANY modification:
1. Have you examined ALL relevant files?
2. Are you using tools one at a time and waiting for results?
3. Have you confirmed success of EACH step before proceeding?
4. Are you about to modify a critical component?
5. Will your changes affect package structure?
6. Have you validated context persistence?
7. Have you considered calibration impacts?

## High-Risk LLM Behaviors to Avoid

### 1. Moving Too Fast
```
DON'T:
- Make multiple changes at once
- Assume success without confirmation
- Skip file examination
- Rush through tool usage
- Ignore package structure
- Skip context validation
- Bypass calibration checks

DO:
- Use one tool at a time
- Wait for user confirmation
- Examine files thoroughly
- Think through implications
- Respect package organization
- Validate context state
- Verify calibration effects
```

### 2. Incomplete Context
```
DON'T:
- Start coding immediately
- Make assumptions about file contents
- Skip reading referenced files
- Ignore system relationships
- Break package imports
- Overlook context markers
- Ignore calibration levels

DO:
- Read all relevant files
- Understand component relationships
- Verify assumptions
- Consider system-wide impact
- Maintain package structure
- Check context persistence
- Validate calibration state
```

### 3. Critical System Relationships

#### Package Structure
```
utils/
├── __init__.py (CRITICAL: Package marker)
├── conversation_manager.py
├── enhanced_conversation_manager.py
├── style_calibrator.py
├── communication_controller.py
├── chat_analysis.py
└── [other utility modules]

↑ PACKAGE INTEGRITY CRITICAL
├── Enables proper imports
├── Maintains module organization
└── Required for system function
```

#### Core Component Dependencies
```
EnhancedConversationManager
↑ CENTRAL COMPONENT - ALL changes affect this
├── Manages ALL conversation processing
├── Controls Claude API interaction
├── Coordinates style and context
├── Maintains message flow integrity
├── Handles context persistence
└── Manages calibration state
    ↓
StyleCalibrator & CommunicationController
↑ CRITICAL for response quality
├── Must maintain differentiation balance
├── Controls scaling behavior
├── Manages system/user separation
└── Affects ALL communication aspects
```

#### Case File Display Structure
```
Case File Display
↑ CRITICAL for context visibility
├── System Instructions
│   └── Raw system rules/parameters sent to Claude
├── User Profile
│   └── Complete YAML profile including metadata
├── Communication Parameters
│   └── Current numerical values and active instructions
├── Active Alerts
│   └── Critical information and restrictions
├── Support System
│   └── Family and professional network details
├── Behavioral Guidance
│   └── Current instructions to Claude
└── System State
    └── Debug information and status

↑ DISPLAY INTEGRITY CRITICAL
├── Maintains context visibility
├── Shows system state
├── Tracks active parameters
└── Enables debugging
```

#### User Profile Impact
```
user-profiles-yaml.txt
↑ DRIVES ENTIRE SYSTEM BEHAVIOR
├── Affects ALL components
├── Structure must be preserved
├── Requires strict validation
├── Uses TTL caching
└── Changes impact:
    ├── Communication style
    ├── Context handling
    ├── UI presentation
    ├── Analytics capabilities
    └── Calibration behavior
```

#### Context Intelligence Flow
```
Slider (0-100) → StyleCalibrator → EnhancedConversationManager
↑ Changes propagate through message system
├── Affects active conversations through:
    ├── Latest calibration message
    ├── [COMMUNICATION UPDATE] markers
    ├── Context persistence
    └── In-conversation instructions
├── Maintains base context via system prompt
├── Preserves conversation markers
└── Modifies:
    ├── Communication style
    ├── Detail levels
    ├── Rapport building
    └── Context depth
```

#### Message System Architecture
```
EnhancedConversationManager
↑ CRITICAL MESSAGE FLOW CONTROL
├── Manages conversation structure:
    ├── System prompt (base context)
    ├── Calibration messages (dynamic updates)
    ├── Context markers (persistence)
    └── User messages (interaction)
├── Message Role Requirements:
    ├── System: Top-level parameter only
    ├── Assistant: For calibration updates
    └── User: For user input
├── Context Requirements:
    ├── Numbered list tracking
    ├── Reference point storage
    ├── Key detail preservation
    └── Conversation memory
└── Calibration Updates:
    ├── Stored as latest_calibration_message
    ├── Included before user messages
    ├── Uses [COMMUNICATION UPDATE] markers
    └── Linear scaling with thresholds
```

#### Critical Implementation Notes
```
Message Flow
↑ PRECISE ORDER CRITICAL
├── System prompt provides base context
├── Latest calibration message included
├── Context markers maintained
├── User message follows
└── Response maintains style based on:
    ├── System instructions
    ├── Latest calibration values
    ├── Context state
    └── [COMMUNICATION UPDATE] markers

Context Persistence
↑ VALIDATION REQUIRED
├── Check context completeness
├── Verify marker integrity
├── Validate profile state
├── Confirm calibration level
└── Ensure memory consistency

Display Updates
↑ SYNCHRONIZATION CRITICAL
├── Verify all sections present
├── Update on context changes
├── Maintain section order
├── Preserve debug information
└── Show real-time state
```

### 4. System State Management

#### Session State
```
Initialization
↑ CRITICAL SEQUENCE
├── Load user profile
├── Create system prompt
├── Initialize calibration
├── Setup context tracking
└── Start conversation flow

Runtime State
↑ MAINTAIN CONSISTENCY
├── Track active sessions
├── Monitor calibration updates
├── Preserve context markers
├── Maintain profile cache
└── Handle errors gracefully
```

#### Error Prevention
```
Before Changes:
├── Verify file contents
├── Check component relationships
├── Understand message flow
├── Consider API requirements
├── Validate context state
└── Test assumptions

During Implementation:
├── Follow precise order
├── Maintain message structure
├── Preserve calibration flow
├── Track context markers
└── Handle all error cases
```

### 5. Documentation Requirements

#### Code Changes
```
Must Document:
├── Purpose of change
├── Impact on message flow
├── Effect on calibration
├── Context implications
└── API compatibility
```

#### System Updates
```
Must Update:
├── Technical documentation
├── Architecture diagrams
├── Message flow descriptions
├── Context handling notes
└── Implementation details
```

## Final Checklist

Before completing ANY changes:
1. Have you maintained message flow integrity?
2. Are calibration updates properly handled?
3. Is the system prompt structure preserved?
4. Are all message roles correct?
5. Is context persistence validated?
6. Are profile validations complete?
7. Is documentation complete and accurate?
8. Are all Case File sections properly updated?
9. Is display synchronization maintained?
10. Are debug capabilities preserved?
