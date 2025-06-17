"""
Streamlit UI for the Alaska Department of Snow Chatbot.

This module provides a web-based user interface for interacting with the chatbot.
It handles:
- Displaying the chat interface
- Managing chat history using Streamlit session state
- Processing user inputs
- Displaying chatbot responses
"""

import streamlit as st

from src.chatbot_service import call_agent

st.title("Alaska Department of Snow Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about snow removal, road conditions, or other Alaska Department of Snow services..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
 
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = call_agent(prompt)
        st.markdown(response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
