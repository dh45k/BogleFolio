"""
Shared components and utilities for all pages
"""
import streamlit as st
from utils.boglebot import create_boglebot_ui

def display_boglebot_sidebar():
    """Display the Boglebot in a sidebar container"""
    
    # Create an expander for the Boglebot
    with st.expander("💬 Bogleheads Chatbot", expanded=False):
        create_boglebot_ui()

def display_quote():
    """Display a random Jack Bogle quote"""
    quotes = [
        {
            "text": "The greatest enemy of a good plan is the dream of a perfect plan.",
            "author": "Jack Bogle"
        },
        {
            "text": "Don't look for the needle in the haystack. Just buy the haystack!",
            "author": "Jack Bogle"
        },
        {
            "text": "Simplicity is the master key to financial success.",
            "author": "Jack Bogle"
        },
        {
            "text": "Your success in investing will depend in part on your character and guts, and in part on your ability to realize, at the height of ebullience and the depth of despair alike, that this too, shall pass.",
            "author": "Jack Bogle"
        },
        {
            "text": "If you have trouble imagining a 20% loss in the stock market, you shouldn't be in stocks.",
            "author": "Jack Bogle"
        },
        {
            "text": "The stock market is a giant distraction from the business of investing.",
            "author": "Jack Bogle"
        },
        {
            "text": "Time is your friend; impulse is your enemy.",
            "author": "Jack Bogle"
        }
    ]
    
    # Use the current page name as a seed to get a consistent quote per page
    page_name = st.session_state.page
    quote_index = hash(page_name) % len(quotes)
    quote = quotes[quote_index]
    
    st.markdown('<div class="quote-box">', unsafe_allow_html=True)
    st.markdown(f'<p class="quote-text">"{quote["text"]}"</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="quote-author">— {quote["author"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)