import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data.fund_data import get_fund_data, get_fund_alternatives

def show_allocation_page(portfolio):
    """
    Display the portfolio allocation page
    """
    st.header("Portfolio Allocation")
    
    # Get fund data
    fund_data = get_fund_data()
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Asset Allocation")
        
        # Display sliders for allocation percentages
        us_stocks = st.slider(
            "US Stocks (%)", 
            min_value=0, max_value=100, 
            value=portfolio.us_stock_allocation,
            step=1,
            key="us_stocks_slider"
        )
        
        international_stocks = st.slider(
            "International Stocks (%)", 
            min_value=0, max_value=100, 
            value=portfolio.international_stock_allocation,
            step=1,
            key="intl_stocks_slider"
        )
        
        bonds = st.slider(
            "Bonds (%)", 
            min_value=0, max_value=100, 
            value=portfolio.bond_allocation,
            step=1,
            key="bonds_slider"
        )
        
        # Calculate total allocation
        total_allocation = us_stocks + international_stocks + bonds
        
        if total_allocation != 100:
            st.warning(f"Total allocation: {total_allocation}%. Please adjust to equal 100%.")
        else:
            # Update portfolio if allocation has changed
            if (us_stocks != portfolio.us_stock_allocation or 
                international_stocks != portfolio.international_stock_allocation or 
                bonds != portfolio.bond_allocation):
                
                portfolio.update_allocation(us_stocks, international_stocks, bonds)
                st.success("Portfolio allocation updated!")
                
        st.divider()
        
        # Fund selection
        st.subheader("Fund Selection")
        
        # US Stock Fund Selection
        us_stock_options = fund_data[fund_data['Category'].isin(['US Total Market', 'US Large Cap'])]
        us_fund = st.selectbox(
            "US Stock Fund",
            options=us_stock_options['Ticker'].tolist(),
            index=us_stock_options['Ticker'].tolist().index(portfolio.us_stock_fund) 
                if portfolio.us_stock_fund in us_stock_options['Ticker'].tolist() else 0,
            format_func=lambda x: f"{x} - {us_stock_options[us_stock_options['Ticker'] == x]['Fund Name'].values[0]} " +
                                f"({us_stock_options[us_stock_options['Ticker'] == x]['Expense Ratio'].values[0]:.3%})"
        )
        
        # International Stock Fund Selection
        intl_stock_options = fund_data[fund_data['Category'].isin(['International Developed', 'International Emerging'])]
        intl_fund = st.selectbox(
            "International Stock Fund",
            options=intl_stock_options['Ticker'].tolist(),
            index=intl_stock_options['Ticker'].tolist().index(portfolio.international_stock_fund) 
                if portfolio.international_stock_fund in intl_stock_options['Ticker'].tolist() else 0,
            format_func=lambda x: f"{x} - {intl_stock_options[intl_stock_options['Ticker'] == x]['Fund Name'].values[0]} " +
                                 f"({intl_stock_options[intl_stock_options['Ticker'] == x]['Expense Ratio'].values[0]:.3%})"
        )
        
        # Bond Fund Selection
        bond_options = fund_data[fund_data['Category'].isin(['US Total Bond', 'US Treasury', 'US Corporate', 'US TIPS'])]
        bond_fund = st.selectbox(
            "Bond Fund",
            options=bond_options['Ticker'].tolist(),
            index=bond_options['Ticker'].tolist().index(portfolio.bond_fund) 
                if portfolio.bond_fund in bond_options['Ticker'].tolist() else 0,
            format_func=lambda x: f"{x} - {bond_options[bond_options['Ticker'] == x]['Fund Name'].values[0]} " +
                                f"({bond_options[bond_options['Ticker'] == x]['Expense Ratio'].values[0]:.3%})"
        )
        
        # Update portfolio if fund selection has changed
        if (us_fund != portfolio.us_stock_fund or 
            intl_fund != portfolio.international_stock_fund or 
            bond_fund != portfolio.bond_fund):
            
            portfolio.update_funds(us_fund, intl_fund, bond_fund)
            st.success("Fund selection updated!")
        
    with col2:
        # Portfolio visualization
        st.subheader("Portfolio Visualization")
        
        # Get allocation data
        allocation_data = portfolio.get_allocation_data()
        df = pd.DataFrame(allocation_data)
        
        # Create pie chart for allocation
        fig = px.pie(
            df, 
            values='Allocation',
            names='Category',
            title='Asset Allocation',
            color='Category',
            color_discrete_map={
                'US Stocks': '#1f77b4',
                'International Stocks': '#ff7f0e',
                'Bonds': '#2ca02c'
            },
            hover_data=['Fund']
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Display fund information
        st.subheader("Fund Information")
        
        fund_info = pd.DataFrame({
            'Asset Class': ['US Stocks', 'International Stocks', 'Bonds'],
            'Ticker': [portfolio.us_stock_fund, portfolio.international_stock_fund, portfolio.bond_fund],
            'Allocation': [f"{portfolio.us_stock_allocation}%", f"{portfolio.international_stock_allocation}%", f"{portfolio.bond_allocation}%"],
            'Expense Ratio': [
                f"{fund_data[fund_data['Ticker'] == portfolio.us_stock_fund]['Expense Ratio'].values[0]:.3%}",
                f"{fund_data[fund_data['Ticker'] == portfolio.international_stock_fund]['Expense Ratio'].values[0]:.3%}",
                f"{fund_data[fund_data['Ticker'] == portfolio.bond_fund]['Expense Ratio'].values[0]:.3%}"
            ]
        })
        
        st.dataframe(fund_info, use_container_width=True)
        
        # Calculate and display weighted expense ratio
        weighted_expense = portfolio.get_weighted_expense_ratio()
        st.metric("Portfolio Weighted Expense Ratio", f"{weighted_expense:.4%}")
        
    # Account values section
    st.divider()
    st.subheader("Account Values")
    
    # Create columns for account inputs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        account_401k = st.number_input(
            "401(k) Value ($)",
            min_value=0,
            value=portfolio.account_values.get("401k", 0),
            step=1000
        )
    
    with col2:
        account_ira = st.number_input(
            "IRA Value ($)",
            min_value=0,
            value=portfolio.account_values.get("IRA", 0),
            step=1000
        )
    
    with col3:
        account_hsa = st.number_input(
            "HSA Value ($)",
            min_value=0,
            value=portfolio.account_values.get("HSA", 0),
            step=1000
        )
    
    with col4:
        account_taxable = st.number_input(
            "Taxable Account Value ($)",
            min_value=0,
            value=portfolio.account_values.get("Taxable", 0),
            step=1000
        )
    
    # Update account values if changed
    updated_accounts = {
        "401k": account_401k,
        "IRA": account_ira,
        "HSA": account_hsa,
        "Taxable": account_taxable
    }
    
    if updated_accounts != portfolio.account_values:
        portfolio.update_account_values(updated_accounts)
        st.success("Account values updated!")
    
    # Display account allocation pie chart
    account_df = pd.DataFrame({
        'Account': list(portfolio.account_values.keys()),
        'Value': list(portfolio.account_values.values())
    })
    
    # Only show pie chart if there are non-zero account values
    if sum(account_df['Value']) > 0:
        fig = px.pie(
            account_df,
            values='Value',
            names='Account',
            title='Account Distribution',
            color='Account',
            color_discrete_map={
                '401k': '#636EFA',
                'IRA': '#EF553B',
                'HSA': '#00CC96',
                'Taxable': '#AB63FA'
            }
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Enter account values to see distribution.")
    
    # Add Jack Bogle quotes
    st.divider()
    st.markdown("""
    > *"Never underrate the importance of asset allocation."* - Jack Bogle
    
    > *"Don't look for the needle in the haystack. Just buy the haystack."* - Jack Bogle
    """, unsafe_allow_html=True)
    
    # Add Bogleheads information and resources
    st.divider()
    st.subheader("Bogleheads")
    
    st.markdown("""
    Bogleheads are passive investors who follow Jack Bogle's simple but powerful message to diversify with low-cost index funds and let compounding grow wealth. Jack founded Vanguard and pioneered indexed mutual funds. His work has since inspired others to get the most out of their long-term investments. Active managers want your money - our advice: keep it! How? Investing in broad-market low-cost indexes, diversified between equities and fixed income. Buy, hold, pay low fees, and stay the course!
    """)
    
    st.subheader("Bogleheads Community Subreddit and Blog")
    st.markdown("""
    [Bogleheads Subreddit](https://www.reddit.com/r/Bogleheads/)  
    [Bogleheads.org](https://www.bogleheads.org/)
    """)
    
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
    
    # Keep the full YouTube video embedded
    st.subheader("Featured Video")
    st.video("https://youtube.com/watch?v=PN6uKE_vbWs", start_time=0)
    st.caption("How to Have the Perfect Portfolio in Investment - John Bogle's view")
