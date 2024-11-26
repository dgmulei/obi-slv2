# Testing Chat Storage System

## Local Environment Setup

1. Create a `.env` file in the project root:
```env
GCS_BUCKET_NAME=your-bucket-name
# Option 1: Path to service account JSON file
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
# Option 2: Or paste the entire JSON content
# GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", ...}
```

2. Install test dependencies:
```bash
pip install pytest python-dotenv google-cloud-storage
```

## Running Tests

1. Basic test run:
```bash
python tests/test_chat_storage.py
```

2. Expected output:
```
Test thread ID: <uuid>

Testing thread storage...
✓ Thread saved successfully

Testing thread retrieval...
✓ Thread retrieved successfully
✓ Found 2 messages

Testing thread update...
✓ Thread updated successfully
✓ Now has 3 messages

Testing date range retrieval...
✓ Found 1 threads in last 5 minutes

All tests passed successfully!
```

## Troubleshooting

1. GCS Credentials Error:
```
❌ Error: GCS credentials not found in environment variables
```
Solution: Check your `.env` file has either `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_APPLICATION_CREDENTIALS_JSON`

2. Bucket Name Error:
```
❌ Error: GCS_BUCKET_NAME not found in environment variables
```
Solution: Add `GCS_BUCKET_NAME=your-bucket-name` to `.env`

3. Permission Errors:
```
❌ Test failed: 403 Forbidden
```
Solution: Verify service account has Storage Object Viewer and Creator roles

## Verifying Stored Data

1. View in GCS Console:
   - Go to your GCS bucket
   - Navigate to `chat-histories/`
   - You should see JSON files named with UUIDs

2. File Content Example:
```json
{
    "thread_id": "uuid",
    "timestamp": "2024-03-21T10:30:00Z",
    "messages": [
        {
            "role": "user",
            "content": "Hello, I need help with license renewal",
            "timestamp": "2024-03-21T10:30:00Z",
            "visible": true
        },
        {
            "role": "assistant",
            "content": "I can help you with that. What type of license do you currently have?",
            "timestamp": "2024-03-21T10:30:01Z",
            "visible": true
        }
    ]
}
```

## Next Steps

After verifying local functionality:

1. Add the environment variables to Streamlit Cloud:
   - GCS_BUCKET_NAME
   - GOOGLE_APPLICATION_CREDENTIALS_JSON

2. Deploy your app
3. Monitor the first few conversations to ensure proper storage
4. Use chat_retrieval.py to analyze stored conversations
