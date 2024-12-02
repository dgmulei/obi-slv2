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
        try:
            # Display personal information with fallbacks
            personal = user.get('personal', {})
            st.write(f"Name: {personal.get('full_name', 'Not provided')}")
            if 'dob' in personal:
                st.write(f"DOB: {personal['dob']}")
                
            # Display license information with fallbacks
            license_info = user.get('license', {})
            license_number = license_info.get('license_number', 'Not provided')
            expiration_date = license_info.get('expiration_date', 'Not provided')
            
            st.write(f"License Number: {license_number}")
            st.write(f"Expiration: {expiration_date}")
            
        except Exception as e:
            logger.error(f"Error displaying user info: {str(e)}")
            st.error("Error displaying user information")

def _format_section(title: str, content: str) -> str:
    """Format a section with title and content."""
    return f"### {title}\n\n```text\n{content}\n```"

def get_case_file_content(context: ConversationContext, conversation_manager: ConversationManager) -> Optional[str]:
    """Get the formatted case file content showing Claude's Tier One memory."""
    try:
        if not context.active_user_profile:
            return None
            
        # Get the enhanced manager for this context
        enhanced_manager = conversation_manager.session_manager.enhanced_managers.get(context.thread_id)
        if not enhanced_manager or not enhanced_manager.system_prompt:
            return None
            
        formatted_sections = []
        
        # 1. System Instructions
        system_rules = enhanced_manager.system_prompt.split('USER PROFILE')[0].strip()
        formatted_sections.append(_format_section("SYSTEM INSTRUCTIONS", system_rules))
        
        # 2. User Profile
        profile_yaml = context.active_user_profile
        formatted_sections.append(_format_section("USER PROFILE", str(profile_yaml)))
        
        # 3. Communication Parameters
        comm_params = []
        
        # Add current numerical values
        if enhanced_manager.current_project_folder and hasattr(enhanced_manager.current_project_folder, 'calibrated_controls'):
            controls = enhanced_manager.current_project_folder.calibrated_controls
            comm_params.append("Current Values:")
            for key, value in controls.items():
                comm_params.append(f"{key}: {value}")
            comm_params.append("")
        
        # Add active instructions
        if enhanced_manager.latest_calibration_message:
            content = enhanced_manager.latest_calibration_message['content']
            content = content.replace("[COMMUNICATION UPDATE] ", "")
            comm_params.append("Active Instructions:")
            comm_params.extend(content.split('\n'))
        
        formatted_sections.append(_format_section("COMMUNICATION PARAMETERS", '\n'.join(comm_params)))
        
        return '\n\n'.join(formatted_sections)
        
    except Exception as e:
        logger.error(f"Error getting case file content: {str(e)}")
        return None

def process_user_message(message: str, conversation_manager: ConversationManager, context: ConversationContext, visible: bool = True) -> bool:
    """Process user message and get response."""
    try:
        # Get assistant's response
        response_content, success = conversation_manager.get_response(
            message, 
            context,
            visible=visible
        )
        
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
            }
            
            /* Code block styling */
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
