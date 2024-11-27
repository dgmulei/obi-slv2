# OBI-SLv2 (Refactoring Development Version)

This is version 2 of the OBI-SL project, focused on enhancing Obi's contextual intelligence capabilities. This development branch explores how to transform static user data into rich, actionable insights that drive more meaningful interactions.

## Core Innovation: Context Intelligence

Obi's key innovation is its ability to derive deep situational understanding from standard bureaucratic data. Rather than relying on explicit user preferences or questionnaires, the system:

1. Analyzes Static Data Points
   - Documentation history
   - Transaction patterns
   - Family support structures
   - Professional context
   - Service interaction patterns

2. Builds Rich Behavioral Profiles
   For example, from basic license renewal data, Obi can understand that a user:
   - Needs step-by-step guidance (derived from age + paper preferences)
   - Values efficiency (inferred from profession + payment methods)
   - Has specific support needs (analyzed from family assistance patterns)
   - Requires particular attention areas (determined from restriction history)

3. Adapts Communication Dynamically
   The Context Intelligence slider controls how deeply Obi analyzes and responds to derived insights, transforming typically unused data into meaningful interaction patterns.

### Context Intelligence Slider

The Context Intelligence slider (0-100%) controls how strongly Obi applies its situational analysis:

#### Scale Effects
- **0% (Minimum)**: Basic interaction (1-1-1)
  - Minimal personalization
  - Standard responses
  - Basic service information

- **60% (Default)**: Balanced interaction (3-3-3)
  - Moderate personalization
  - Context-aware responses
  - Tailored guidance

- **100% (Maximum)**: Deep interaction (5-5-5)
  - Full personalization
  - Highly context-aware
  - Deeply tailored support

#### Communication Metrics (1-5 Scale)
1. **Interaction Style**
   - Level of engagement and conversational depth
   - Affects how Obi structures its responses

2. **Detail Level**
   - Depth of information provided
   - Complexity of explanations

3. **Rapport Level**
   - Degree of relationship building
   - Attention to personal context

#### Real-time Updates
- Slider changes immediately affect:
  - Case Files display
  - System prompts
  - AI response patterns
- Changes propagate through:
  - StyleCalibrator
  - EnhancedConversationManager
  - Active conversations

## System Components

### Context Analysis Engine
- Transforms standard bureaucratic data into behavioral insights
- Identifies support systems and potential challenges
- Builds comprehensive situation awareness without user input

### Adaptive Communication Controller
- Adjusts interaction patterns based on derived context
- Manages communication depth and complexity
- Adapts to situation-specific requirements

### StyleCalibrator
- Calibrates communication values on 1-5 scale
- Translates slider position (0-100%) to interaction metrics
- Ensures consistent scaling across all conversations

### EnhancedConversationManager
- Maintains project folder with current calibration
- Updates system prompts based on calibrated values
- Ensures AI responses reflect current context settings

### Chat Storage System

#### Thread Creation
- New UUID generated for each conversation
- Stored in GCS as `chat-histories/{thread_id}.json`

#### Message Storage
- All user and assistant messages stored
- System messages excluded
- Timestamps in UTC
- Messages marked with visibility flag

#### Data Structure
```json
{
    "thread_id": "unique-uuid",
    "timestamp": "2024-03-21T10:30:00Z",
    "messages": [
        {
            "role": "user",
            "content": "message content",
            "timestamp": "2024-03-21T10:30:00Z",
            "visible": true
        },
        {
            "role": "assistant",
            "content": "response content",
            "timestamp": "2024-03-21T10:30:01Z",
            "visible": true
        }
    ]
}
```

## Setup Instructions

1. Create a Google Cloud Project
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable the Cloud Storage API

2. Create a Storage Bucket
   ```bash
   # Using Google Cloud CLI
   gcloud storage buckets create gs://your-bucket-name
   ```
   Or create via the web console:
   - Go to Cloud Storage > Buckets
   - Click "Create Bucket"
   - Choose a unique name
   - Select "Standard" storage class
   - Choose a region (preferably same as Streamlit Cloud)

3. Create Service Account
   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Name: "chat-storage-sa"
   - Role: "Storage Object Viewer" and "Storage Object Creator"
   - Create and download JSON key file

4. Set Environment Variables in Streamlit Cloud
   Add these to your app settings:
   ```
   GCS_BUCKET_NAME=your-bucket-name
   GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", ... } # Paste entire JSON key content
   ```

## Usage Examples

### Retrieve Chat Threads

```python
from datetime import datetime, timezone, timedelta
from utils.chat_retrieval import get_chat_thread, get_threads_by_date_range

# Get a single thread
thread = get_chat_thread("thread-id-here")
print(f"Thread messages: {len(thread['messages'])}")

# Get last week's threads
end = datetime.now(timezone.utc)
start = end - timedelta(days=7)
threads = get_threads_by_date_range(start, end)

# Basic analysis
for thread in threads:
    print(f"Thread ID: {thread['thread_id']}")
    print(f"Message count: {len(thread['messages'])}")
    print(f"Duration: {thread['messages'][-1]['timestamp']} - {thread['messages'][0]['timestamp']}")
```

## Security Notes

- Service account has minimal permissions (object viewer/creator only)
- All data stored in your GCS bucket
- No PII stored beyond chat content
- Threads identified by UUID only
