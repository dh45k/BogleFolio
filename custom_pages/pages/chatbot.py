import streamlit as st
import os
from utils.chatbot import get_chatbot_response, get_allocation_advice, get_fund_comparison

def show_chatbot_page():
    """
    Display the AI Investment Assistant chatbot page
    """
    # Page header
    st.markdown('<h1 style="color:#1E5631;">AI Investment Assistant</h1>', unsafe_allow_html=True)
    
    # Jack Bogle quote
    st.markdown(
        """
        <div class="quote-box">
            <p class="quote-text">"The idea that a bell rings to signal when investors should get into or out of the stock market is simply not credible. After nearly fifty years in this business, I do not know of anybody who has done it successfully and consistently."</p>
            <p class="quote-author">— John C. Bogle</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Introduction
    st.markdown("""
    This AI assistant helps answer your investment questions following Boglehead principles - focusing on 
    low-cost index funds, proper asset allocation, and long-term investing strategies.
    """)
    
    # Check if OpenAI API key is available
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    if not openai_api_key:
        st.warning("""
        **OpenAI API Key Not Found**
        
        The AI Assistant requires an OpenAI API key to function. Without this key, the chatbot and investment tools cannot provide responses.
        
        Please add your OpenAI API key to continue using this feature.
        """)
        st.markdown("### How to Get an OpenAI API Key")
        st.markdown("""
        1. Visit [OpenAI's Platform](https://platform.openai.com/signup)
        2. Create an account or sign in
        3. Navigate to the API Keys section
        4. Create a new secret key
        5. Add the key to this application
        """)
        return
        
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about investing..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = get_chatbot_response(st.session_state.messages)
                    st.markdown(response)
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    response = error_msg
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Specialized tools
    st.markdown("### Specialized Investment Tools")
    
    # Two-column layout for tools
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Asset Allocation Advisor")
        with st.expander("Get personalized allocation advice"):
            age = st.number_input("Your age", min_value=18, max_value=100, value=35)
            risk_tolerance = st.selectbox(
                "Risk Tolerance", 
                options=["Low", "Medium", "High"],
                index=1
            )
            financial_situation = st.text_area(
                "Brief description of your financial situation",
                placeholder="e.g., Stable job, emergency fund in place, saving for retirement in 30 years",
                max_chars=500
            )
            
            if st.button("Get Allocation Advice"):
                with st.spinner("Generating advice..."):
                    try:
                        advice = get_allocation_advice(age, risk_tolerance, financial_situation)
                        st.markdown(advice)
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_msg)
    
    with col2:
        st.markdown("#### Fund Comparison Tool")
        with st.expander("Compare investment funds"):
            fund_info = st.text_area(
                "Enter fund details to compare",
                placeholder="e.g., Fund 1: VTI, Expense Ratio: 0.03%, AUM: $1.2T\nFund 2: ITOT, Expense Ratio: 0.03%, AUM: $350B",
                max_chars=1000,
                height=150
            )
            
            if st.button("Compare Funds"):
                with st.spinner("Analyzing funds..."):
                    try:
                        comparison = get_fund_comparison(fund_info)
                        st.markdown(comparison)
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_msg)
    
    # Educational resources
    st.markdown("### Educational Resources")
    st.markdown("""
    - [Bogleheads.org](https://www.bogleheads.org/) - Community forum for Boglehead investors
    - [Bogleheads Wiki](https://www.bogleheads.org/wiki/Main_Page) - Comprehensive resource on investing
    - [Bogleheads® Investment Philosophy](https://www.bogleheads.org/wiki/Bogleheads%C2%AE_investment_philosophy) - Core principles
    - [Three-fund portfolio](https://www.bogleheads.org/wiki/Three-fund_portfolio) - Simple investing approach
    """)
    
    # Disclaimer
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; font-size: 0.8rem;">
        <strong>Disclaimer:</strong> This AI assistant provides general investing information based on Boglehead principles, 
        not personalized investment advice. Consult with a qualified financial advisor for advice tailored to your specific situation.
    </div>
    """, unsafe_allow_html=True)