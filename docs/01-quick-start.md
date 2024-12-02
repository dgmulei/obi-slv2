# Obi - Massachusetts RMV Service Agent

An AI-powered service agent that provides personalized assistance for Massachusetts driver's license renewals. The system combines rich user profiling with contextual intelligence to deliver highly adaptive interactions.

## Key Features

### 1. Personalized Assistance
- Dynamic user profiling with TTL caching
- Context-aware responses with persistence
- Adaptive communication styles (1-5 scale):
  * Interaction Style: methodical (1) to efficient (5)
  * Detail Level: maximum (1) to minimal (5)
  * Rapport Level: personal (1) to professional (5)
- Real-time style adjustments
- Strict profile validation

### 2. Context Intelligence
- Slider-based context control (0-100)
- User preferences preserved (1-5 scale)
- Clean system/user preference separation
- Three application levels:
  * MINIMAL (0-30): Consider preferences as minor adjustments
  * MODERATE (31-70): Balance preferences with protocol
  * STRICT (71-100): Make preferences primary guide
- Reliable context preservation
- Conversation memory tracking

### 3. Document Integration
- RMV documentation integration
- Intelligent document retrieval
- Context-aware information delivery
- Real-time document reference
- Persistent reference tracking

## Installation

### 1. Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### 2. Configuration
```bash
# Required environment variables
export ANTHROPIC_API_KEY=your_api_key
export GCS_BUCKET_NAME=your_bucket_name
export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### 3. Document Setup
```bash
# Create required directories
mkdir -p data/drivers_license_docs
mkdir -p chroma_db
mkdir -p .streamlit
```

## Basic Usage

### 1. Start the Application
```bash
# Run the development server
streamlit run dev/run_local.py
```

### 2. User Interface
- **Context Intelligence Slider**: Adjust interaction depth (0-100)
  * MINIMAL (0-30): Consider preferences as minor adjustments
  * MODERATE (31-70): Balance preferences with protocol
  * STRICT (71-100): Make preferences primary guide
- **Dual Citizen Interface**: Manage multiple conversations
- **Enhanced Case File Display**: View comprehensive context:
  1. FORMATTED SUMMARY
     - Critical License Information
     - Documentation Status
     - Payment Information
     - Personal Information
     - Latest Communication Update
  2. CLAUDE'S CONTEXT
     - System Instructions
     - User Profile
     - Communication Parameters
       * Current Values
       * Latest Update showing:
         - User preferences (1-5 scale)
         - Behavioral guidance
         - Application level (MINIMAL/MODERATE/STRICT)
- **Chat Interface**: Interact with Obi

### 3. Context Control
- Low (0-30): MINIMAL ADHERENCE
  * Start with standardized procedures
  * Consider preferences as minor adjustments
  * Keep responses protocol-focused
  * Use context only when directly relevant

- Medium (31-70): MODERATE ADHERENCE
  * Balance procedures with preferences
  * Incorporate preferred style while maintaining protocol
  * Adapt responses while staying process-focused
  * Use context to enhance understanding

- High (71-100): STRICT ADHERENCE
  * Make preferences primary guide
  * Fully embrace preferred style
  * Maximize personalization while professional
  * Actively use context for relevance

## Development

### 1. Project Structure
```
obi-slv2/
├── app.py                 # Main application
├── utils/                 # Core utilities
│   ├── conversation_manager.py
│   ├── enhanced_conversation_manager.py
│   ├── style_calibrator.py
│   └── ...
├── data/                 # Document storage
├── docs/                 # Documentation
└── tests/                # Test suite
```

### 2. Key Components
- **ConversationManager**: Handles chat flow and context
- **EnhancedConversationManager**: Manages context and calibration
- **StyleCalibrator**: Controls adaptation and scaling
- **QueryEngine**: Manages documents and references
- **ProfileManager**: Handles profile validation and caching

### 3. Testing
```bash
# Run test suite
python -m pytest tests/

# Run specific tests
python -m pytest tests/test_chat_storage.py
```

## User Profiles

### 1. Profile Structure
```yaml
users:
  - personal:
      full_name: str
      primary_language: str
  - metadata:
      communication_preferences:
        interaction_style: int  # 1 (methodical) to 5 (efficient)
        detail_level: int      # 1 (maximum) to 5 (minimal)
        rapport_level: int     # 1 (personal) to 5 (professional)
```

### 2. Profile Management
- Stored in user-profiles-yaml.txt
- Strict validation with type checking
- TTL caching for performance
- Drives system behavior
- Affects communication style
- Influences context handling

## Document System

### 1. Supported Documents
- Driver's Manual
- License Applications
- Documentation Checklists
- Fee Schedules

### 2. Document Processing
- Automatic text extraction
- Embedding generation
- Context-aware retrieval
- Real-time reference
- Reference point tracking
- Persistent markers

## Security

### 1. API Security
- Secure key management
- Rate limiting
- Error handling
- Access control
- Profile protection

### 2. Data Protection
- Encrypted storage
- Secure transmission
- Profile protection
- Document security
- Cache security
- Context protection

## Monitoring

### 1. System Logs
- API interactions
- Error tracking
- Performance metrics
- Usage statistics
- Context persistence
- Profile validation

### 2. Analytics
- Conversation analysis
- Profile effectiveness
- Context intelligence impact
- User engagement
- Calibration effectiveness
- Memory persistence

## Troubleshooting

### 1. Common Issues
- API connection errors
- Document processing issues
- Profile loading problems
- Context adaptation errors
- Calibration issues
- Memory persistence failures

### 2. Solutions
- Check environment variables
- Verify file permissions
- Review log files
- Confirm API status
- Validate profile data
- Check context state

## Support

### 1. Documentation
- Technical Reference
- System Architecture
- LLM Context Guide
- Human Context Guide

### 2. Resources
- Source code
- Issue tracker
- Development guides
- API documentation
- Profile guidelines
- Context management guides
