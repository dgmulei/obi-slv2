# Patch SQLite before any other imports
import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

import streamlit as st
import logging
from utils.conversation_manager import ConversationContext
from utils.config import initialize_components, load_user_profiles
from utils.ui_components import (
    display_chat_messages,
    display_user_info,
    process_user_message,
    setup_case_file_css,
    display_case_file,
    get_case_file_content
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.set_page_config(
        page_title="Obi - Driver's License Renewal Guide",
        page_icon="🪪",
        layout="wide"
    )
    
    # Add custom CSS for slider spacing and expander
    st.markdown("""
        <style>
        .stSlider {
            padding-top: 2rem;
        }
        .personality-info {
            margin-top: 1rem;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize components first
    if 'components' not in st.session_state:
        embeddings_manager, query_engine, conversation_manager = initialize_components(60)
        st.session_state.components = {
            'embeddings_manager': embeddings_manager,
            'query_engine': query_engine,
            'conversation_manager': conversation_manager
        }
        st.session_state.last_differentiation = 60
    
    # Initialize session states
    if 'citizen1_context' not in st.session_state:
        st.session_state.citizen1_context = ConversationContext(
            messages=[], 
            system_message_added=False,
            active_user_profile=None
        )
    
    if 'citizen2_context' not in st.session_state:
        st.session_state.citizen2_context = ConversationContext(
            messages=[],
            system_message_added=False,
            active_user_profile=None
        )
    
    # Initialize message keys if not present
    if 'citizen1_message_key' not in st.session_state:
        st.session_state.citizen1_message_key = 0
    if 'citizen2_message_key' not in st.session_state:
        st.session_state.citizen2_message_key = 0
    
    # Add Context Intelligence slider with default value of 60
    differentiation = st.slider(
        "Context Intelligence",
        0, 100, st.session_state.last_differentiation,
        help="Adjust how deeply Obi analyzes and responds to each person's unique situation"
    )
    
    # Handle slider changes
    if differentiation != st.session_state.last_differentiation:
        logger.info(f"Differentiation level changed from {st.session_state.last_differentiation} to {differentiation}")
        # Update conversation manager
        st.session_state.components['conversation_manager'].differentiation_level = differentiation
        st.session_state.last_differentiation = differentiation
        st.rerun()  # Always rerun on slider change to ensure UI updates
    
    # Add collapsible info section
    with st.expander("🔍 How Context Intelligence Works", expanded=False):
        st.markdown("""
        #### What This Dial Controls
        - **Response Intelligence**: From standard system responses (0) to deeply contextual interaction that understands and adapts to your complete situation (100)
        - **Situational Awareness**: How Obi interprets and responds to your unique circumstances
        - **Communication Depth**: Adjusts explanation style based on your background and needs
        - **Interaction Pattern**: Adapts to your situation-specific requirements
        
        #### What Obi Analyzes
        - **Life Context**: Automatically understands your situation from available information
        - **Time Constraints**: Recognizes and adapts to your schedule demands
        - **Support Network**: Identifies and considers family/professional support systems
        - **Documentation Status**: Analyzes your current document validity and requirements
        """)
    
    # Check if collection is empty and show appropriate message
    collection = st.session_state.components['embeddings_manager'].get_collection()
    if collection.count() == 0:
        st.warning("No documents have been added to the system yet. The chatbot will have limited functionality until documents are added.")
    
    # Load user profiles
    user_profiles = load_user_profiles()
    
    # Set up CSS for case file display
    setup_case_file_css()
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown("### Case Files")
        # Display case files in sidebar tabs
        content1 = get_case_file_content(st.session_state.citizen1_context, st.session_state.components['conversation_manager'])
        content2 = get_case_file_content(st.session_state.citizen2_context, st.session_state.components['conversation_manager'])
        display_case_file(content1, content2)
    
    # ===== MAIN CONTENT =====
    st.markdown("<h1 style='text-align: center;'>Obi</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #666666;'>Massachusetts RMV Service Agent</h3>", unsafe_allow_html=True)
    
    # Create two columns for the chat interfaces
    col1, col2 = st.columns(2)
    
    # Citizen 1 Column
    with col1:
        if user_profiles["users"]:
            display_user_info(user_profiles["users"][0])
        
        # Start button
        start1 = st.button("Start Citizen 1", use_container_width=True)
        
        # Display messages
        display_chat_messages(st.session_state.citizen1_context.messages)
        
        # Handle start button click
        if start1 and user_profiles["users"]:
            st.session_state.citizen1_context.active_user_profile = user_profiles["users"][0]
            st.session_state.citizen1_context.messages = []
            st.session_state.citizen1_context.system_message_added = False
            if process_user_message("Hello?", st.session_state.components['conversation_manager'], st.session_state.citizen1_context):
                st.rerun()  # Rerun to update UI after processing
        
        # Chat input (only show if we have messages)
        if st.session_state.citizen1_context.messages:
            chat_input_key = f"chat_input_1_{st.session_state.citizen1_message_key}"
            
            if prompt := st.chat_input("Type your message here...", key=chat_input_key):
                # Update message key first
                st.session_state.citizen1_message_key += 1
                
                # Process message
                if process_user_message(prompt, st.session_state.components['conversation_manager'], st.session_state.citizen1_context):
                    st.rerun()  # Rerun to update UI after processing
    
    # Citizen 2 Column
    with col2:
        if len(user_profiles["users"]) > 1:
            display_user_info(user_profiles["users"][1])
        
        # Start button
        start2 = st.button("Start Citizen 2", use_container_width=True)
        
        # Display messages
        display_chat_messages(st.session_state.citizen2_context.messages)
        
        # Handle start button click
        if start2 and len(user_profiles["users"]) > 1:
            st.session_state.citizen2_context.active_user_profile = user_profiles["users"][1]
            st.session_state.citizen2_context.messages = []
            st.session_state.citizen2_context.system_message_added = False
            if process_user_message("Hello?", st.session_state.components['conversation_manager'], st.session_state.citizen2_context):
                st.rerun()  # Rerun to update UI after processing
        
        # Chat input (only show if we have messages)
        if st.session_state.citizen2_context.messages:
            chat_input_key = f"chat_input_2_{st.session_state.citizen2_message_key}"
            
            if prompt := st.chat_input("Type your message here...", key=chat_input_key):
                # Update message key first
                st.session_state.citizen2_message_key += 1
                
                # Process message
                if process_user_message(prompt, st.session_state.components['conversation_manager'], st.session_state.citizen2_context):
                    st.rerun()  # Rerun to update UI after processing

if __name__ == "__main__":
    main()
