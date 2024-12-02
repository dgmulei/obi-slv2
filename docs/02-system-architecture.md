# Obi System Overview

## System Architecture

```mermaid
graph TD
    A[Streamlit App] --> B[ConversationManager]
    B --> C[EnhancedConversationManager]
    B --> D[ChatStorage]
    
    subgraph "Profile System"
        E[user-profiles-yaml.txt] --> F[Profile Loader]
        F --> B
        F --> C
        G[Profile Cache] --> F
    end
    
    subgraph "Context Intelligence"
        H[StyleCalibrator] --> C
        I[CommunicationController] --> C
        J[Context Slider] --> H
        K[ConversationMarkers] --> C
    end
    
    subgraph "Document System"
        L[EmbeddingsManager] --> M[ChromaDB]
        N[QueryEngine] --> M
        N --> C
    end
    
    subgraph "Storage System"
        D --> O[Google Cloud Storage]
        P[ChatRetrieval] --> O
        Q[utils/chat_analysis.py] --> P
    end

    subgraph "Case File Display"
        R[System Instructions] --> S[UI Components]
        T[User Profile] --> S
        U[Communication Parameters] --> S
        V[Active Alerts] --> S
        W[Support System] --> S
        X[Behavioral Guidance] --> S
        Y[System State] --> S
        S --> A
    end
```

## Core Components Interaction

```mermaid
sequenceDiagram
    participant U as User
    participant App as Streamlit App
    participant CM as ConversationManager
    participant ECM as EnhancedConversationManager
    participant SC as StyleCalibrator
    participant CC as ConversationContext
    participant QE as QueryEngine
    participant CS as ChatStorage
    participant CF as Case File Display

    U->>App: Send Message
    App->>CM: Process Message
    CM->>ECM: Get Response
    ECM->>SC: Get Style Calibration
    ECM->>CC: Validate Context
    ECM->>QE: Get Relevant Documents
    ECM->>CF: Update Display Sections
    ECM->>U: Return Response
    CM->>CS: Store Conversation
```

## System Components

### 1. User Interface Layer
- **Streamlit App (app.py)**
  - Dual-citizen interface
  - Context Intelligence slider (0-100)
  - Enhanced Case File display with sections:
    - System Instructions
    - User Profile
    - Communication Parameters
    - Active Alerts
    - Support System
    - Behavioral Guidance
    - System State
  - Real-time chat interface

### 2. Profile Management
- **User Profiles (user-profiles-yaml.txt)**
  ```yaml
  users:
    - personal:
        full_name: str
        primary_language: str
    - metadata:
        communication_preferences:
          interaction_style: int
          detail_level: int
          rapport_level: int
  ```
- Drives system behavior
- Influences all component interactions
- Profile caching with TTL
- Strict validation enforcement

### 3. Conversation Processing

```mermaid
graph LR
    A[ConversationManager] --> B[EnhancedConversationManager]
    B --> C[ConversationContext]
    B --> D[Claude API]
    B --> E[Style System]
    B --> F[Case File Display]
    
    subgraph "Style System"
        E --> G[StyleCalibrator]
        E --> H[CommunicationController]
    end

    subgraph "Context System"
        C --> I[Numbered Lists]
        C --> J[Reference Points]
        C --> K[Key Details]
    end

    subgraph "Case File Sections"
        F --> L[System Instructions]
        F --> M[User Profile]
        F --> N[Communication Parameters]
        F --> O[Active Alerts]
        F --> P[Support System]
        F --> Q[Behavioral Guidance]
        F --> R[System State]
    end
```

### 4. Document Management

```mermaid
graph TD
    A[EmbeddingsManager] --> B[Text Processing]
    B --> C[Embedding Generation]
    C --> D[ChromaDB Storage]
    E[QueryEngine] --> D
```

### 5. Storage Architecture

```mermaid
graph TD
    A[ChatStorage] --> B[GCS]
    C[ChatRetrieval] --> B
    D[utils/chat_analysis.py] --> C
    
    subgraph "Data Structure"
        B --> E[thread_id.json]
        E --> F[Thread Data]
        F --> G[Messages]
        F --> H[User Profile ID]
        F --> I[Timestamps]
        F --> J[Context Markers]
    end
```

### 6. Context Intelligence Flow

```mermaid
sequenceDiagram
    participant U as User
    participant S as Slider
    participant SC as StyleCalibrator
    participant ECM as EnhancedConversationManager
    participant CC as ConversationContext
    participant CF as Case File Display
    participant C as Claude API

    U->>S: Adjust Slider
    S->>SC: Update Value
    SC->>ECM: Calibrate Controls
    ECM->>CC: Update Context
    ECM->>ECM: Create Calibration Message
    Note over ECM: Stores as latest_calibration_message
    ECM->>CF: Update Display Sections
    ECM->>C: Next Message Flow
    Note over C: Includes calibration + context + user message
```

```
Slider Input (0-100) → Style Calibration → Context Update →
Calibration Message Creation → Display Update → Message Integration → Response Adaptation
```

### 7. Message Flow Architecture

```mermaid
graph TD
    A[System Prompt] --> E[Claude API]
    B[Latest Calibration] --> C[Message Array]
    D[User Message] --> C
    F[Context Markers] --> C
    C --> E
    
    subgraph "Message Components"
        A
        B
        D
        F
    end
    
    subgraph "Integration"
        C
        E
    end
```

Key Components:
1. System Prompt
   - Base context and rules
   - Communication preferences
   - User profile information

2. Calibration Messages
   - Role: assistant
   - Format: [COMMUNICATION UPDATE]
   - Contains latest calibration values
   - Overrides previous calibrations

3. Context Markers
   - Numbered lists tracking
   - Reference points
   - Key details storage
   - Conversation memory

4. Message Integration
   - Latest calibration included before user message
   - Context markers maintained
   - Clear update markers for LLM recognition
   - Maintains conversation continuity

## Data Flows

### 1. Conversation Flow
```
User Input → Profile Loading → Context Validation → Style Calibration → 
Document Retrieval → Response Generation → Display Update → Storage
```

### 2. Context Intelligence Flow
```
Slider Input (0-100) → Style Calibration → Communication Control →
Context Update → Enhanced Manager → Display Update → Response Adaptation
```

### 3. Analysis Flow
```
Chat Retrieval → Thread Processing → Context Analysis →
Profile Analysis → Usage Patterns → Insights Generation
```

## System Integration Points

### 1. Profile Integration
- Loaded during initialization
- Cached with TTL
- Influences all components
- Drives communication style
- Affects document retrieval

### 2. Context Intelligence
- Real-time calibration
- Profile-aware adaptation
- Dynamic response styling
- Contextual understanding
- Linear scaling with thresholds
- Clean system/user separation

### 3. Storage Integration
- Profile-linked threads
- Context-aware retrieval
- Analysis capabilities
- Security measures
- Context persistence

### 4. Display Integration
- Real-time section updates
- Context-aware content
- Profile-driven information
- System state monitoring
- Debug information display
- Alert status tracking

## Development Considerations

### 1. Local Development
```bash
# Run development server
streamlit run dev/run_local.py

# Run analysis
python utils/chat_analysis.py [days]

# Run tests
python -m pytest tests/
```

### 2. Environment Setup
```bash
# Required variables
ANTHROPIC_API_KEY=key
GCS_BUCKET_NAME=bucket
GOOGLE_APPLICATION_CREDENTIALS=path
```

### 3. Security Measures
- Profile data protection
- Secure API handling
- Minimal permissions
- Encrypted storage
- Cache security

## Monitoring and Analysis

### 1. System Metrics
- Thread counts
- Response times
- Profile statistics
- Usage patterns
- Context persistence
- Calibration effectiveness

### 2. Analysis Tools
- Chat history analysis
- Profile effectiveness
- Context intelligence impact
- User engagement metrics
- Context maintenance metrics

## Future Considerations

### 1. Scalability
- Profile system expansion
- Enhanced analytics
- Additional integrations
- Performance optimization
- Context tracking improvements

### 2. Enhancements
- Profile automation
- Advanced analytics
- Extended document support
- Integration capabilities
- Context persistence optimization
