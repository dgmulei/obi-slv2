"""UI components and helper functions."""

import streamlit as st
import logging
import textwrap
from typing import Dict, Any, Optional, List
from .conversation_manager import ConversationManager, ConversationContext, Message

logger = logging.getLogger(__name__)

def display_chat_messages(messages: List[Message]) -> None:
    """Display chat messages excluding system messages."""
    for message in messages:
        if message.role != "system" and message.visible:
            with st.chat_message(message.role):
                st.markdown(message.content)

def display_user_info(user: Dict[str, Any]) -> None:
    """Display user information in a collapsible expander."""
    with st.expander("User Information", expanded=False):
        st.write(f"Name: {user['personal']['full_name']}")
        st.write(f"DOB: {user['personal']['dob']}")
        st.write(f"License Number: {user['license']['current']['number']}")
        st.write(f"Expiration: {user['license']['current']['expiration']}")

def get_case_file_content(context: ConversationContext, conversation_manager: ConversationManager) -> Optional[str]:
    """Get the formatted case file content from the project folder."""
    try:
        if not context.active_user_profile:
            return None
            
        # Get the enhanced manager for this context
        enhanced_manager = conversation_manager.session_manager.enhanced_managers.get(context.thread_id)
        if not enhanced_manager or not enhanced_manager.system_prompt:
            return None
            
        # Split the system prompt into sections
        sections = enhanced_manager.system_prompt.split('\n\n')
        formatted_sections = []
        
        for section in sections:
            # Skip empty sections
            if not section.strip():
                continue
                
            # Get section title and content
            lines = section.split('\n')
            title = lines[0].strip(':')
            content = '\n'.join(lines[1:])
            
            # Update section titles with subheaders
            if title == "SYSTEM RULES (NON-NEGOTIABLE)":
                title = "SYSTEM RULES\nCore Service Parameters"
            elif title == "USER CONTEXT":
                title = "USER CONTEXT\nDerived from Static Data"
            elif title == "COMMUNICATION PREFERENCES":
                title = "COMMUNICATION PREFERENCES\nAI-Analyzed Patterns"
            elif title == "USER PROFILE SUMMARY":
                # Simply replace the all-caps header with title case
                content = content.replace("STRUCTURED COMMUNICATION REQUIREMENTS:", "Structured Communication Requirements:")
                title = "USER PROFILE SUMMARY\nSynthesized Understanding"
            
            # Format list items and regular content differently
            formatted_lines = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    # Format list items with proper indentation and wrapping
                    wrapped = textwrap.fill(line[2:], width=50, initial_indent='• ', subsequent_indent='  ')
                    formatted_lines.append(wrapped)
                else:
                    # Format regular content with proper wrapping
                    if line:  # Only process non-empty lines
                        wrapped = textwrap.fill(line, width=50)
                        formatted_lines.append(wrapped)
            
            # Format section with improved markdown
            formatted_section = f"### {title}\n\n```text\n" + '\n'.join(formatted_lines) + "\n```"
            formatted_sections.append(formatted_section)
        
        # Combine all sections with proper spacing
        return '\n\n'.join(formatted_sections)
    except Exception as e:
        logger.error(f"Error getting case file content: {str(e)}")
        return None

def process_user_message(message: str, conversation_manager: ConversationManager, context: ConversationContext, visible: bool = True) -> bool:
    """Process user message and get response."""
    try:
        # Create and add user message first
        user_message = Message(role="user", content=message, visible=visible)
        context.messages.append(user_message)
        
        # Get assistant's response
        response_content, success = conversation_manager.get_response(
            message, 
            context,
            visible=visible
        )
        
        if success:
            # Create and add assistant message
            assistant_message = Message(role="assistant", content=response_content, visible=visible)
            context.messages.append(assistant_message)
            
            # For initial "Hello?" message, make it invisible after successful response
            if message == "Hello?":
                user_message.visible = False
        
        return success
            
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return False

def setup_case_file_css() -> None:
    """Set up CSS for the case file display."""
    st.markdown("""
        <style>
            /* Sidebar styling */
            section[data-testid="stSidebar"] {
                width: 600px !important;
                background-color: #f8f9fa;
                padding: 1rem;
            }
            
            section[data-testid="stSidebar"] > div {
                padding: 0;
            }
            
            /* Sidebar header */
            section[data-testid="stSidebar"] h3 {
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid #dee2e6;
            }
            
            /* Tab styling */
            .stTabs {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            
            .stTabs [data-baseweb="tab-list"] {
                gap: 0;
                background-color: #f1f3f5;
                padding: 0.5rem 0.5rem 0;
                border-radius: 8px 8px 0 0;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 40px;
                padding: 0 16px;
                margin-right: 4px;
                border-radius: 4px 4px 0 0;
            }
            
            .stTabs [data-baseweb="tab-panel"] {
                padding: 1rem;
                max-height: calc(100vh - 200px);
                overflow-y: auto;
            }
            
            /* Case file content styling */
            .case-file {
                font-size: 0.9rem;
                line-height: 1.5;
                width: 100%;
                box-sizing: border-box;
            }
            
            .case-file h3 {
                color: #2c3e50;
                font-size: 1.1rem;
                margin: 1.5rem 0 1rem 0;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid #eaecef;
                white-space: pre-line;
            }
            
            /* Code block styling with improved wrapping */
            .case-file pre {
                background-color: white;
                border: 1px solid #eaecef;
                border-radius: 6px;
                padding: 1rem;
                margin: 0.75rem 0;
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
                font-size: 0.85rem;
                line-height: 1.6;
                white-space: pre-wrap !important;
                word-wrap: break-word !important;
                overflow-wrap: break-word !important;
                width: 100% !important;
                box-sizing: border-box !important;
                display: block !important;
            }
            
            .case-file code {
                white-space: pre-wrap !important;
                word-wrap: break-word !important;
                overflow-wrap: break-word !important;
                width: 100% !important;
                box-sizing: border-box !important;
                display: inline-block !important;
                color: #24292e;
            }
            
            /* Main content styling */
            .main .block-container {
                padding-top: 2rem;
                max-width: 1200px;
            }
            
            /* Chat interface styling */
            .stChatMessage {
                background-color: white;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            
            /* Hide default Streamlit elements */
            .stDeployButton, .viewerBadge_container__1QSob {
                display: none !important;
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8;
            }
            
            /* Additional wrapper styling */
            .stMarkdown {
                width: 100% !important;
            }
            
            .stMarkdown > div {
                width: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)

def display_case_file(content1: Optional[str], content2: Optional[str]) -> None:
    """Display the case file content in the sidebar with tabs."""
    tab1, tab2 = st.tabs(["Citizen 1", "Citizen 2"])
    
    with tab1:
        if content1:
            st.markdown('<div class="case-file">', unsafe_allow_html=True)
            st.markdown(content1)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Start conversation to view case file")
    
    with tab2:
        if content2:
            st.markdown('<div class="case-file">', unsafe_allow_html=True)
            st.markdown(content2)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Start conversation to view case file")
