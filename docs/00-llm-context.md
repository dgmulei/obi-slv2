# LLM Context Guide

⚠️ CRITICAL: This document is designed specifically for LLMs. READ THIS FIRST before making any changes to the system.

## STOP AND THINK

Before ANY modification:
1. Have you examined ALL relevant files?
2. Are you using tools one at a time and waiting for results?
3. Have you confirmed success of EACH step before proceeding?
4. Are you about to modify a critical component?
5. Will your changes affect package structure?

## High-Risk LLM Behaviors to Avoid

### 1. Moving Too Fast
```
DON'T:
- Make multiple changes at once
- Assume success without confirmation
- Skip file examination
- Rush through tool usage
- Ignore package structure

DO:
- Use one tool at a time
- Wait for user confirmation
- Examine files thoroughly
- Think through implications
- Respect package organization
```

### 2. Incomplete Context
```
DON'T:
- Start coding immediately
- Make assumptions about file contents
- Skip reading referenced files
- Ignore system relationships
- Break package imports

DO:
- Read all relevant files
- Understand component relationships
- Verify assumptions
- Consider system-wide impact
- Maintain package structure
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
└── Maintains message flow integrity
    ↓
StyleCalibrator & CommunicationController
↑ CRITICAL for response quality
├── Must maintain differentiation balance
└── Affects ALL communication aspects
```

#### User Profile Impact
```
user-profiles-yaml.txt
↑ DRIVES ENTIRE SYSTEM BEHAVIOR
├── Affects ALL components
├── Structure must be preserved
└── Changes impact:
    ├── Communication style
    ├── Context handling
    ├── UI presentation
    └── Analytics capabilities
```

#### Context Intelligence Flow
```
Slider (0-100) → StyleCalibrator → EnhancedConversationManager
↑ Changes propagate through message system
├── Affects active conversations through:
    ├── Latest calibration message
    ├── [COMMUNICATION UPDATE] markers
    └── In-conversation instructions
├── Maintains base context via system prompt
└── Modifies:
    ├── Communication style
    ├── Detail levels
    └── Rapport building
```

#### Message System Architecture
```
EnhancedConversationManager
↑ CRITICAL MESSAGE FLOW CONTROL
├── Manages conversation structure:
    ├── System prompt (base context)
    ├── Calibration messages (dynamic updates)
    └── User messages (interaction)
├── Message Role Requirements:
    ├── System: Top-level parameter only
    ├── Assistant: For calibration updates
    └── User: For user input
└── Calibration Updates:
    ├── Stored as latest_calibration_message
    ├── Included before user messages
    └── Uses [COMMUNICATION UPDATE] markers
```

#### Critical Implementation Notes
```
Message Flow
↑ PRECISE ORDER CRITICAL
├── System prompt provides base context
├── Latest calibration message included
├── User message follows
└── Response maintains style based on:
    ├── System instructions
    ├── Latest calibration values
    └── [COMMUNICATION UPDATE] markers
```

### 4. System State Management

#### Session State
```
Initialization
↑ CRITICAL SEQUENCE
├── Load user profile
├── Create system prompt
├── Initialize calibration
└── Start conversation flow

Runtime State
↑ MAINTAIN CONSISTENCY
├── Track active sessions
├── Monitor calibration updates
├── Preserve message order
└── Handle errors gracefully
```

#### Error Prevention
```
Before Changes:
├── Verify file contents
├── Check component relationships
├── Understand message flow
├── Consider API requirements
└── Test assumptions

During Implementation:
├── Follow precise order
├── Maintain message structure
├── Preserve calibration flow
└── Handle all error cases
```

### 5. Documentation Requirements

#### Code Changes
```
Must Document:
├── Purpose of change
├── Impact on message flow
├── Effect on calibration
└── API compatibility
```

#### System Updates
```
Must Update:
├── Technical documentation
├── Architecture diagrams
├── Message flow descriptions
└── Implementation notes
```

## Final Checklist

Before completing ANY changes:
1. Have you maintained message flow integrity?
2. Are calibration updates properly handled?
3. Is the system prompt structure preserved?
4. Are all message roles correct?
5. Is documentation complete and accurate?
