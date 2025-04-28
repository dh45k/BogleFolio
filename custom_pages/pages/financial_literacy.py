import streamlit as st

def show_financial_literacy_page():
    """
    Display the financial literacy page with Bogleheads resources, quotes,
    and educational content about Jack Bogle's investment philosophy.
    """
    st.header("Financial Literacy")
    
    # Jack Bogle quotes
    st.subheader("Investment Wisdom from Jack Bogle")
    st.markdown("""
    > *"Never underrate the importance of asset allocation."* - Jack Bogle
    
    > *"Don't look for the needle in the haystack. Just buy the haystack."* - Jack Bogle
    
    > *"The grim irony of investing is that we investors as a group not only don't get what we pay for, we get precisely what we don't pay for."* - Jack Bogle
    
    > *"Stay the course. No matter what happens, stick to your program. I've said 'stay the course' a thousand times, and I meant it every time."* - Jack Bogle
    
    > *"Time is your friend; impulse is your enemy."* - Jack Bogle
    """, unsafe_allow_html=True)
    
    # Bogleheads information
    st.subheader("The Bogleheads Philosophy")
    
    st.markdown("""
    Bogleheads are passive investors who follow Jack Bogle's simple but powerful message to:
    
    1. **Diversify with low-cost index funds**
    2. **Let compounding grow your wealth over time** 
    3. **Stay the course through market volatility**
    
    Jack Bogle founded Vanguard and pioneered indexed mutual funds. His work has inspired millions of investors to get the most out of their long-term investments. 
    
    Active managers want your money - the Bogleheads' advice: keep it! How? Invest in broad-market low-cost indexes, diversify between equities and fixed income, buy, hold, pay low fees, and stay the course!
    """)
    
    # Core principles
    st.subheader("Core Bogleheads Principles")
    
    st.markdown("""
    1. **Live Below Your Means** - Saving a significant portion of income is the foundation of investment success
    2. **Develop a Workable Plan** - Set investment goals and develop a plan to achieve them
    3. **Never Bear Too Much or Too Little Risk** - Find an appropriate asset allocation that lets you sleep at night
    4. **Diversify** - Use broadly diversified, low-cost index funds to capture market returns
    5. **Never Try to Time the Market** - Stay the course and avoid emotional reactions to market movements
    6. **Use Index Funds** - The most reliable way to capture market returns is by using low-cost index funds
    7. **Keep Costs Low** - Expenses directly reduce returns, so minimize them
    8. **Minimize Taxes** - Use tax-advantaged accounts and tax-efficient fund placement
    9. **Invest for the Long Term** - Focus on decades, not weeks or months
    10. **Stay the Course** - Develop a sound plan and stick with it, ignoring financial noise
    """)
    
    # Community resources
    st.subheader("Bogleheads Community Resources")
    st.markdown("""
    - [Bogleheads.org Forum](https://www.bogleheads.org/forum/index.php) - A vibrant community of investors discussing Bogle's principles
    - [Bogleheads Wiki](https://www.bogleheads.org/wiki/Main_Page) - Comprehensive resource for Bogleheads investing knowledge
    - [Bogleheads Subreddit](https://www.reddit.com/r/Bogleheads/) - Reddit community discussing passive index investing
    - [Bogleheads on Investing Podcast](https://bogleheads.podbean.com/) - Hosted by Rick Ferri, featuring interviews with key figures in passive investing
    """)
    
    # Jack Bogle's Words in YouTube Videos
    st.subheader("Jack Bogle's Words in YouTube Videos")
    
    # Shorts as links
    st.markdown("""
    - [John Bogle: Important Rule For Investors](https://youtube.com/shorts/2zlrR6lXDJ0?si=HAephkTl49npWM-n)
    - [WARREN BUFFETT JACK BOGLE](https://youtube.com/shorts/8v3jBQSod_A?si=KjGLq5kv8i3sJ8ks)
    - [John Bogle: How to Get Rich Investing?](https://youtube.com/shorts/qyLoTOhMjSM?si=ROPoR3fGpN2-Yb_k)
    - [Jack BOGLE: Invest For A LIFETIME #jackbogle](https://youtube.com/shorts/9ZPcVeS9LOE?si=QECz6Hs8stZq-cTX)
    - [Jack Bogle on how to handle market declines](https://youtube.com/shorts/n4N45Dk5c9M?si=KE2SIatgq59cu_2w)
    - [Jack Bogle's Money Advice](https://youtube.com/shorts/woOxKtYX-2I?si=KAf5EJvq4Y1IOaIR)
    - [Don't time the market. "Jack Bogle: Stay The Course."](https://youtube.com/shorts/zaEBrWCJyPo?si=bfaa4S5CJUnAkXW2)
    """)
    
    # Featured video
    st.subheader("Featured Video")
    st.video("https://youtube.com/watch?v=PN6uKE_vbWs", start_time=0)
    st.caption("How to Have the Perfect Portfolio in Investment - John Bogle's view")
    
    # Book recommendations
    st.subheader("Essential Reading")
    
    book_col1, book_col2, book_col3 = st.columns(3)
    
    with book_col1:
        st.markdown("### The Little Book of Common Sense Investing")
        st.markdown("*by John C. Bogle*")
        st.markdown("The classic guide to Bogle's strategy of index fund investing. A must-read for every Boglehead.")
        
    with book_col2:
        st.markdown("### The Bogleheads' Guide to Investing")
        st.markdown("*by Taylor Larimore, Mel Lindauer, and Michael LeBoeuf*")
        st.markdown("A practical, hands-on guide to implementing Bogle's investment strategy.")
        
    with book_col3:
        st.markdown("### A Random Walk Down Wall Street")
        st.markdown("*by Burton G. Malkiel*")
        st.markdown("A classic explanation of why markets are efficient and why index investing works.")