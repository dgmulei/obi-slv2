# Obi - Massachusetts RMV Service Agent

An AI-powered service agent that provides personalized assistance for Massachusetts driver's license renewals. The system combines rich user profiling with contextual intelligence to deliver highly adaptive interactions.

## Key Features

### 1. Personalized Assistance
- Dynamic user profiling
- Context-aware responses
- Adaptive communication styles
- Real-time style adjustments

### 2. Context Intelligence
- Slider-based context control (0-100)
- Real-time communication adaptation
- Situation-aware responses
- Dynamic style calibration

### 3. Document Integration
- RMV documentation integration
- Intelligent document retrieval
- Context-aware information delivery
- Real-time document reference

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
- **Dual Citizen Interface**: Manage multiple conversations
- **Case File Display**: View conversation context
- **Chat Interface**: Interact with Obi

### 3. Context Control
- Low (0-30): Standard system responses
- Medium (31-70): Contextual adaptation
- High (71-100): Deep personalization

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
- **ConversationManager**: Handles chat flow
- **EnhancedConversationManager**: Manages context
- **StyleCalibrator**: Controls adaptation
- **QueryEngine**: Manages documents

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
        interaction_style: int
        detail_level: int
        rapport_level: int
```

### 2. Profile Management
- Stored in user-profiles-yaml.txt
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

## Security

### 1. API Security
- Secure key management
- Rate limiting
- Error handling
- Access control

### 2. Data Protection
- Encrypted storage
- Secure transmission
- Profile protection
- Document security

## Monitoring

### 1. System Logs
- API interactions
- Error tracking
- Performance metrics
- Usage statistics

### 2. Analytics
- Conversation analysis
- Profile effectiveness
- Context intelligence impact
- User engagement

## Troubleshooting

### 1. Common Issues
- API connection errors
- Document processing issues
- Profile loading problems
- Context adaptation errors

### 2. Solutions
- Check environment variables
- Verify file permissions
- Review log files
- Confirm API status

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
