import os
import sys
from datetime import datetime, timezone, timedelta
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.chat_storage import ChatStorage
from utils.chat_retrieval import get_chat_thread, get_threads_by_date_range

def test_chat_storage():
    """Test basic chat storage and retrieval functionality."""
    
    # Create test messages
    test_messages = [
        {
            "role": "user",
            "content": "Hello, I need help with license renewal",
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            "visible": True
        },
        {
            "role": "assistant",
            "content": "I can help you with that. What type of license do you currently have?",
            "timestamp": (datetime.now(timezone.utc) + timedelta(seconds=1)).isoformat() + "Z",
            "visible": True
        }
    ]
    
    try:
        # Initialize storage
        storage = ChatStorage()
        
        # Generate test thread ID
        thread_id = str(uuid.uuid4())
        print(f"\nTest thread ID: {thread_id}")
        
        # Test saving thread
        print("\nTesting thread storage...")
        storage.save_thread(test_messages, thread_id)
        print("✓ Thread saved successfully")
        
        # Test retrieving thread
        print("\nTesting thread retrieval...")
        retrieved_thread = get_chat_thread(thread_id)
        assert retrieved_thread["thread_id"] == thread_id
        assert len(retrieved_thread["messages"]) == len(test_messages)
        print("✓ Thread retrieved successfully")
        print(f"✓ Found {len(retrieved_thread['messages'])} messages")
        
        # Test updating thread
        print("\nTesting thread update...")
        new_message = {
            "role": "user",
            "content": "I have a Class D license",
            "timestamp": (datetime.now(timezone.utc) + timedelta(seconds=2)).isoformat() + "Z",
            "visible": True
        }
        test_messages.append(new_message)
        storage.update_thread(thread_id, test_messages)
        
        # Verify update
        updated_thread = get_chat_thread(thread_id)
        assert len(updated_thread["messages"]) == len(test_messages)
        print("✓ Thread updated successfully")
        print(f"✓ Now has {len(updated_thread['messages'])} messages")
        
        # Test date range retrieval
        print("\nTesting date range retrieval...")
        end = datetime.now(timezone.utc)
        start = end - timedelta(minutes=5)
        threads = get_threads_by_date_range(start, end)
        print(f"✓ Found {len(threads)} threads in last 5 minutes")
        
        print("\nAll tests passed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Check for GCS credentials
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        print("\n❌ Error: GCS credentials not found in environment variables")
        print("Please set GOOGLE_APPLICATION_CREDENTIALS in your .env file")
        sys.exit(1)
        
    if not os.getenv('GCS_BUCKET_NAME'):
        print("\n❌ Error: GCS_BUCKET_NAME not found in environment variables")
        sys.exit(1)
    
    test_chat_storage()
