import streamlit as st
from custom_pages.pages.shared import display_quote, display_boglebot_sidebar

def show_financial_literacy_page():
    """
    Display the financial literacy page with educational content
    """
    st.header("Financial Literacy")
    
    # Display a Bogle quote
    display_quote()
    
    # Add the Boglebot chat interface
    display_boglebot_sidebar()
    
    # Introduction
    st.markdown("""
    Financial literacy is the foundation of sound investing. This page provides resources 
    to help you better understand the Bogleheads investment philosophy and key financial concepts.
    """)
    
    # Video section
    st.subheader("Educational Videos")
    
    # Featured video with explanation
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.video("https://youtube.com/watch?v=PN6uKE_vbWs", start_time=0)
    
    with col2:
        st.markdown("""
        ### How to Have the Perfect Portfolio
        
        In this video, John Bogle shares his timeless wisdom on building a successful investment portfolio.
        Key points:
        - Focus on low-cost index funds
        - Maintain broad diversification
        - Stay the course during market volatility
        - Avoid market timing and stock picking
        """)
    
    # Jack Bogle section
    st.subheader("Jack Bogle's Investment Philosophy")
    
    st.markdown("""
    John C. "Jack" Bogle (1929-2019) was the founder of The Vanguard Group and creator of the first index 
    mutual fund available to individual investors. He was a fierce advocate for everyday investors and 
    championed the following core principles:
    
    1. **Invest with simplicity** - Complex strategies and products often lead to worse results
    2. **Keep costs low** - High fees compound over time and significantly reduce returns
    3. **Buy the whole market** - Own broad market index funds rather than trying to pick winners
    4. **Stay the course** - Markets fluctuate, but maintaining your strategy during volatility is crucial
    5. **Invest for the long-term** - Time in the market is more important than timing the market
    """)
    
    # Bogle quotes section
    st.subheader("Wisdom from Jack Bogle")
    
    quotes_col1, quotes_col2 = st.columns(2)
    
    with quotes_col1:
        st.markdown("""
        > *"The simplest and most efficient investment strategy is to buy and hold all of the nation's publicly held businesses at very low cost. The classic index fund that owns this market portfolio is the only investment that guarantees you with your fair share of stock market returns."*
        
        > *"The stock market is a giant distraction to the business of investing."*
        
        > *"In investing, you get what you don't pay for."*
        """)
    
    with quotes_col2:
        st.markdown("""
        > *"Don't look for the needle in the haystack. Just buy the haystack."*
        
        > *"Never underrate the importance of asset allocation."*
        
        > *"Investing is a virtuous habit best started as early as possible."*
        """)
    
    # Bogleheads Community section
    st.subheader("Bogleheads Community")
    
    st.markdown("""
    Bogleheads are passive investors who follow Jack Bogle's simple but powerful message to diversify with low-cost 
    index funds and let compounding grow wealth. Jack founded Vanguard and pioneered indexed mutual funds. His work 
    has since inspired others to get the most out of their long-term investments. Active managers want your money - 
    our advice: keep it! How? Investing in broad-market low-cost indexes, diversified between equities and fixed income. 
    Buy, hold, pay low fees, and stay the course!
    """)
    
    # Resources section
    st.subheader("Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Communities
        - [Bogleheads Forum](https://www.bogleheads.org/forum/index.php)
        - [Bogleheads Subreddit](https://www.reddit.com/r/Bogleheads/)
        - [Bogleheads Wiki](https://www.bogleheads.org/wiki/Main_Page)
        """)
    
    with col2:
        st.markdown("""
        ### Books
        - The Little Book of Common Sense Investing by John C. Bogle
        - The Bogleheads' Guide to Investing by Taylor Larimore, Mel Lindauer, Michael LeBoeuf
        - A Random Walk Down Wall Street by Burton G. Malkiel
        """)
    
    with col3:
        st.markdown("""
        ### Calculators & Tools
        - [Portfolio Visualizer](https://www.portfoliovisualizer.com/)
        - [Vanguard Retirement Nest Egg Calculator](https://retirementplans.vanguard.com/VGApp/pe/pubeducation/calculators/RetirementNestEggCalc.jsf)
        - [Investor.gov Compound Interest Calculator](https://www.investor.gov/financial-tools-calculators/calculators/compound-interest-calculator)
        """)
    
    # Short video clips section
    st.subheader("Jack Bogle Short Clips")
    
    st.markdown("""
    - [John Bogle: Important Rule For Investors](https://youtube.com/shorts/2zlrR6lXDJ0?si=HAephkTl49npWM-n)
    - [WARREN BUFFETT JACK BOGLE](https://youtube.com/shorts/8v3jBQSod_A?si=KjGLq5kv8i3sJ8ks)
    - [John Bogle: How to Get Rich Investing?](https://youtube.com/shorts/qyLoTOhMjSM?si=ROPoR3fGpN2-Yb_k)
    - [Jack BOGLE: Invest For A LIFETIME #jackbogle](https://youtube.com/shorts/9ZPcVeS9LOE?si=QECz6Hs8stZq-cTX)
    - [Jack Bogle on how to handle market declines](https://youtube.com/shorts/n4N45Dk5c9M?si=KE2SIatgq59cu_2w)
    - [Jack Bogle's Money Advice](https://youtube.com/shorts/woOxKtYX-2I?si=KAf5EJvq4Y1IOaIR)
    - [Don't time the market. "Jack Bogle: Stay The Course."](https://youtube.com/shorts/zaEBrWCJyPo?si=bfaa4S5CJUnAkXW2)
    """)