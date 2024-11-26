# OBI-SLv2 (Refactoring Development Version)

This is version 2 of the OBI-SL project, created specifically for refactoring experiments with a focus on Obi's behavior. This version is a development branch that allows for significant changes without affecting the original stable version.

## Relationship to Original Project

This is a development version of the original OBI-SL project, created to:
- Experiment with behavioral improvements
- Test significant architectural changes
- Provide a safe environment for major refactoring
- Develop and test new features before potential integration

The original project remains the stable, production version deployed on Streamlit Cloud.

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

### Data Structure

Each thread is stored as a JSON file with this structure:
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

## Implementation Details

1. Thread Creation
   - New UUID generated for each conversation
   - Stored in GCS as `chat-histories/{thread_id}.json`

2. Message Storage
   - All user and assistant messages stored
   - System messages excluded
   - Timestamps in UTC
   - Messages marked with visibility flag

3. Error Handling
   - Storage failures logged but don't interrupt chat flow
   - Automatic retry on common GCS errors

## Security Notes

- Service account has minimal permissions (object viewer/creator only)
- All data stored in your GCS bucket
- No PII stored beyond chat content
- Threads identified by UUID only
