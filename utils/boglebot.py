"""
Bogleheads Chatbot Module
Uses OpenAI's GPT and Trafilatura for fetching web content
"""
import os
import time
import json
import streamlit as st
from openai import OpenAI
import trafilatura
from urllib.parse import urljoin

# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Create OpenAI client with API key from environment variable
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Cache for fetched content to avoid redundant requests
# Format: {url: {"content": content, "timestamp": timestamp}}
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_web_content(url):
    """Fetch content from a URL using trafilatura"""
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return None

def get_bogleheads_resources():
    """Return a list of key Bogleheads resources to search for information"""
    resources = [
        {
            "name": "Bogleheads Investment Philosophy",
            "url": "https://www.bogleheads.org/wiki/Bogleheads%C2%AE_investment_philosophy"
        },
        {
            "name": "Three-fund portfolio",
            "url": "https://www.bogleheads.org/wiki/Three-fund_portfolio"
        },
        {
            "name": "Lazy portfolios",
            "url": "https://www.bogleheads.org/wiki/Lazy_portfolios"
        },
        {
            "name": "Tax-efficient fund placement",
            "url": "https://www.bogleheads.org/wiki/Tax-efficient_fund_placement"
        },
        {
            "name": "Getting started",
            "url": "https://www.bogleheads.org/wiki/Getting_started"
        },
        {
            "name": "Asset allocation",
            "url": "https://www.bogleheads.org/wiki/Asset_allocation"
        }
    ]
    return resources

def get_relevant_content(query, max_resources=3):
    """
    Get relevant content from Bogleheads resources based on the query
    Returns a dictionary of {resource_name: content}
    """
    resources = get_bogleheads_resources()
    
    # First, use OpenAI to determine which resources are most relevant to the query
    try:
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor assistant. Your task is to identify which of these Bogleheads resources would be most relevant to answer a user's question. Return a JSON array of indices (0-based) of the top most relevant resources, with a maximum of 3 resources."},
                {"role": "user", "content": f"Question: {query}\n\nResources:\n" + "\n".join([f"{i}. {res['name']}" for i, res in enumerate(resources)])}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        selected_indices = result.get("indices", [])[:max_resources]
        
        # If no indices were returned, default to the first 2 resources
        if not selected_indices:
            selected_indices = [0, 1]
    except Exception as e:
        print(f"Error determining relevant resources: {e}")
        # Default to the first 2 resources if there's an error
        selected_indices = [0, 1]
    
    # Fetch content from selected resources
    relevant_content = {}
    for idx in selected_indices:
        resource = resources[idx]
        content = fetch_web_content(resource["url"])
        if content:
            relevant_content[resource["name"]] = content
    
    return relevant_content

def answer_question(query):
    """
    Answer a question using OpenAI and relevant Bogleheads content
    """
    # Get relevant content based on the query
    st.session_state.chatbot_status = "Searching Bogleheads resources..."
    relevant_content = get_relevant_content(query)
    
    if not relevant_content:
        return "I'm sorry, I couldn't find relevant information to answer your question. Please try asking differently or check the Bogleheads website directly."
    
    # Prepare context from relevant content
    st.session_state.chatbot_status = "Analyzing information..."
    context = "\n\n".join([f"RESOURCE: {name}\n{content}" for name, content in relevant_content.items()])
    
    # Prepare sources citation
    sources = "Sources: " + ", ".join([name for name in relevant_content.keys()])
    
    try:
        # Get answer from OpenAI
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": """You are a helpful financial advisor specializing in Bogleheads investment philosophy.
                 Answer questions based on the provided context from Bogleheads resources. 
                 Be concise, accurate, and educational.
                 Follow these principles:
                 1. Emphasize long-term, passive investing with low-cost index funds
                 2. Focus on asset allocation and diversification
                 3. Minimize costs and taxes
                 4. Avoid market timing and active stock picking
                 5. Keep explanations simple and understandable
                 
                 If you don't know something or it's not covered in the context, say so honestly.
                 Format your answers in markdown for better readability.
                 Always indicate which resources you referenced in your answer.
                 """},
                {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}"}
            ],
            max_tokens=800
        )
        
        answer = response.choices[0].message.content
        
        # Append sources at the end if not already included
        if "Sources:" not in answer:
            answer = f"{answer}\n\n{sources}"
        
        return answer
    except Exception as e:
        print(f"Error getting answer from OpenAI: {e}")
        return f"I'm having trouble generating an answer right now. Error: {str(e)}"

def create_boglebot_ui():
    """Create the Boglebot chat interface"""
    
    # Initialize chat history in session state if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "chatbot_status" not in st.session_state:
        st.session_state.chatbot_status = ""
    
    # Create a container for the chat interface
    st.markdown("### 💬 Boglebot: Your Bogleheads Investment Assistant")
    st.markdown("Ask questions about investing, asset allocation, or anything related to the Bogleheads investment philosophy.")
    
    # Chat message container
    chat_container = st.container()
    
    # Status indicator
    if st.session_state.chatbot_status:
        st.info(st.session_state.chatbot_status)
    
    # Function to handle sending a message
    def send_message():
        if st.session_state.user_input:
            user_message = st.session_state.user_input
            
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            
            # Clear input
            st.session_state.user_input = ""
            
            # Get response
            bot_response = answer_question(user_message)
            
            # Add bot response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            
            # Clear status
            st.session_state.chatbot_status = ""
    
    # Input field and send button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_input("Your question", key="user_input", on_change=send_message, placeholder="E.g., What is the 3-fund portfolio?")
    with col2:
        st.button("Send", on_click=send_message)
    
    # Display chat history in reverse order (newest at the bottom)
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Boglebot:** {message['content']}")
            
            # Add a divider between messages
            st.markdown("---")
    
    # Add a button to clear chat history
    if st.session_state.chat_history:
        if st.button("Clear Conversation"):
            st.session_state.chat_history = []
            st.rerun()