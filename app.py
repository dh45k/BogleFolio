import streamlit as st
import os
import json
from utils.portfolio import Portfolio

# Set page config
st.set_page_config(
    page_title="Boglehead Portfolio Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = Portfolio()

if 'portfolios' not in st.session_state:
    st.session_state.portfolios = {}

if 'current_portfolio_name' not in st.session_state:
    st.session_state.current_portfolio_name = "Default Portfolio"

# Main app title
st.title("Boglehead 3-Fund Portfolio Optimizer")

# Sidebar for app navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["Portfolio Allocation", "Compound Growth", "Fund Comparison", "Tax Efficiency"]
)

# Portfolio management in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Portfolio Management")

# Save portfolio
portfolio_name = st.sidebar.text_input("Portfolio Name:", value=st.session_state.current_portfolio_name)
if st.sidebar.button("Save Portfolio"):
    st.session_state.portfolios[portfolio_name] = st.session_state.portfolio.to_dict()
    st.session_state.current_portfolio_name = portfolio_name
    st.sidebar.success(f"Portfolio '{portfolio_name}' saved!")

# Load portfolio
if st.session_state.portfolios:
    portfolio_to_load = st.sidebar.selectbox(
        "Select Portfolio to Load:", 
        options=list(st.session_state.portfolios.keys()),
        index=list(st.session_state.portfolios.keys()).index(st.session_state.current_portfolio_name) 
            if st.session_state.current_portfolio_name in st.session_state.portfolios else 0
    )
    
    if st.sidebar.button("Load Portfolio"):
        st.session_state.portfolio = Portfolio.from_dict(st.session_state.portfolios[portfolio_to_load])
        st.session_state.current_portfolio_name = portfolio_to_load
        st.sidebar.success(f"Portfolio '{portfolio_to_load}' loaded!")

# Export/Import portfolios
st.sidebar.markdown("---")
st.sidebar.subheader("Export/Import")

if st.sidebar.button("Export Portfolios"):
    # Convert portfolios to JSON
    portfolio_data = {name: portfolio for name, portfolio in st.session_state.portfolios.items()}
    json_data = json.dumps(portfolio_data)
    
    # Create download button
    st.sidebar.download_button(
        label="Download Portfolio Data",
        data=json_data,
        file_name="boglehead_portfolios.json",
        mime="application/json"
    )

uploaded_file = st.sidebar.file_uploader("Import Portfolios", type=["json"])
if uploaded_file is not None:
    try:
        import_data = json.load(uploaded_file)
        for name, portfolio_data in import_data.items():
            st.session_state.portfolios[name] = portfolio_data
        st.sidebar.success("Portfolios imported successfully!")
    except Exception as e:
        st.sidebar.error(f"Error importing portfolios: {e}")

# Render selected page
if page == "Portfolio Allocation":
    from pages.allocation import show_allocation_page
    show_allocation_page(st.session_state.portfolio)
elif page == "Compound Growth":
    from pages.compound_growth import show_compound_growth_page
    show_compound_growth_page(st.session_state.portfolio)
elif page == "Fund Comparison":
    from pages.fund_comparison import show_fund_comparison_page
    show_fund_comparison_page()
elif page == "Tax Efficiency":
    from pages.tax_efficiency import show_tax_efficiency_page
    show_tax_efficiency_page(st.session_state.portfolio)

# Footer
st.markdown("---")
st.markdown("### About This Tool")
st.markdown("""
This tool is designed for Bogleheads to optimize their 3-fund portfolios. It helps visualize asset allocation, 
project growth over time, compare fund expenses, and optimize tax efficiency across different account types.

Built following Bogleheads investment principles:
- Low-cost index funds
- Broad diversification
- Long-term investment horizon
- Tax-efficient fund placement
""")
