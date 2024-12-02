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
├── Must maintain preference integrity
├── Controls application strength
├── Manages system/user separation
└── Affects ALL communication aspects
```

#### Context Intelligence Flow
```
Slider (0-100) → StyleCalibrator → EnhancedConversationManager
↑ Three-part message structure:
├── Raw Preferences (1-5 scale)
│   ├── Preserved at all levels
│   ├── Interaction Style: methodical (1) to efficient (5)
│   ├── Detail Level: maximum (1) to minimal (5)
│   └── Rapport Level: personal (1) to professional (5)
├── Behavioral Guidance
│   ├── Matches preferences exactly
│   ├── Example for efficient (5):
│   │   ├── "Communicate directly and efficiently"
│   │   ├── "Focus on key points and actions"
│   │   └── "Keep explanations brief and targeted"
└── Application Guidance
    ├── MINIMAL (0-30): Consider preferences as minor adjustments
    ├── MODERATE (31-70): Balance preferences with protocol
    └── STRICT (71-100): Make preferences primary guide
```

#### Case File Display Structure
```
Case File Display
↑ TWO MAIN SECTIONS
├── FORMATTED SUMMARY
│   ├── Critical License Information
│   ├── Documentation Status
│   ├── Payment Information
│   ├── Personal Information
│   └── Latest Communication Update
└── CLAUDE'S CONTEXT
    ├── System Instructions
    ├── User Profile
    └── Communication Parameters
        ├── Current Values
        ├── Latest [COMMUNICATION UPDATE]
        └── Application Guidance

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
├── Communication Preferences (1-5 scale)
│   ├── interaction_style: methodical (1) to efficient (5)
│   ├── detail_level: maximum (1) to minimal (5)
│   └── rapport_level: personal (1) to professional (5)
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

#### Message System Architecture
```
EnhancedConversationManager
↑ CRITICAL MESSAGE FLOW CONTROL
├── [COMMUNICATION UPDATE] Structure:
│   ├── Raw preferences (always preserved)
│   ├── Behavioral guidance (matches preferences)
│   └── Application guidance (varies with level)
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
    └── Application level controls strength
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
    ├── Raw preferences (1-5)
    ├── Behavioral guidance
    └── Application level (MINIMAL/MODERATE/STRICT)

Context Persistence
↑ VALIDATION REQUIRED
├── Check context completeness
├── Verify marker integrity
├── Validate profile state
├── Confirm calibration level
└── Ensure memory consistency

Display Updates
↑ SYNCHRONIZATION CRITICAL
├── Verify both sections present
│   ├── Formatted Summary
│   └── Claude's Context
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
├── Extract preferences (1-5)
├── Create system prompt
├── Initialize calibration
├── Setup context tracking
└── Start conversation flow

Runtime State
↑ MAINTAIN CONSISTENCY
├── Track active sessions
├── Preserve raw preferences
├── Monitor application level
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
├── Preserve preferences
├── Track context markers
└── Handle all error cases
```

### 5. Documentation Requirements

#### Code Changes
```
Must Document:
├── Purpose of change
├── Impact on preferences
├── Effect on application levels
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
2. Are raw preferences preserved?
3. Is the system prompt structure preserved?
4. Are all message roles correct?
5. Is context persistence validated?
6. Are profile validations complete?
7. Is documentation complete and accurate?
8. Are both Case File sections properly updated?
9. Is display synchronization maintained?
10. Are debug capabilities preserved?
