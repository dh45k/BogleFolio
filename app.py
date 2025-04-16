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
    
if 'page' not in st.session_state:
    st.session_state.page = "Portfolio Allocation"

# Main app title
st.title("Boglehead 3-Fund Portfolio Optimizer")

# Main page navigation tabs
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Portfolio Allocation", use_container_width=True):
        st.session_state['page'] = "Portfolio Allocation"
        st.rerun()
with col2:
    if st.button("Compound Growth", use_container_width=True):
        st.session_state['page'] = "Compound Growth"
        st.rerun()
with col3:
    if st.button("Fund Comparison", use_container_width=True):
        st.session_state['page'] = "Fund Comparison"
        st.rerun()
with col4:
    if st.button("Tax Efficiency", use_container_width=True):
        st.session_state['page'] = "Tax Efficiency"
        st.rerun()

st.markdown("---")

# Hide default Streamlit menu and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Custom navigation sidebar without the default pages
st.sidebar.markdown("<h2>Navigation</h2>", unsafe_allow_html=True)
page_options = ["Portfolio Allocation", "Compound Growth", "Fund Comparison", "Tax Efficiency"]
page = st.sidebar.radio(
    "Select page:",
    page_options,
    index=page_options.index(st.session_state.page),
    label_visibility="collapsed"
)
# Update page in session state when changed via sidebar
if page != st.session_state.page:
    st.session_state.page = page
    st.rerun()

# Portfolio management in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Portfolio Management")

# Save portfolio
portfolio_name = st.sidebar.text_input("Portfolio Name:", value=st.session_state.current_portfolio_name)

# Storage options
storage_option = st.sidebar.radio("Storage:", ["Local", "Database"], horizontal=True)

if st.sidebar.button("Save Portfolio"):
    # Always save to local memory
    st.session_state.portfolios[portfolio_name] = st.session_state.portfolio.to_dict()
    st.session_state.current_portfolio_name = portfolio_name
    
    # If database option selected, also save to database
    if storage_option == "Database":
        try:
            from utils.db import save_portfolio
            portfolio_db = save_portfolio(st.session_state.portfolio)
            st.sidebar.success(f"Portfolio '{portfolio_name}' saved to database (ID: {portfolio_db.id})!")
        except Exception as e:
            st.sidebar.error(f"Error saving to database: {str(e)}")
    else:
        st.sidebar.success(f"Portfolio '{portfolio_name}' saved locally!")

# Load portfolio
load_source = st.sidebar.radio("Load from:", ["Local", "Database"], horizontal=True)

if load_source == "Local" and st.session_state.portfolios:
    portfolio_to_load = st.sidebar.selectbox(
        "Select Portfolio to Load:", 
        options=list(st.session_state.portfolios.keys()),
        index=list(st.session_state.portfolios.keys()).index(st.session_state.current_portfolio_name) 
            if st.session_state.current_portfolio_name in st.session_state.portfolios else 0
    )
    
    if st.sidebar.button("Load Local Portfolio"):
        st.session_state.portfolio = Portfolio.from_dict(st.session_state.portfolios[portfolio_to_load])
        st.session_state.current_portfolio_name = portfolio_to_load
        st.sidebar.success(f"Portfolio '{portfolio_to_load}' loaded from local storage!")
        
elif load_source == "Database":
    try:
        from utils.db import get_user_portfolios, load_portfolio
        
        # Get list of portfolios from database
        db_portfolios = get_user_portfolios()
        
        if db_portfolios:
            portfolio_options = [f"{p['name']} (ID: {p['id']})" for p in db_portfolios]
            selected_db_portfolio = st.sidebar.selectbox(
                "Select Database Portfolio:",
                options=portfolio_options
            )
            
            # Extract the ID from the selection
            portfolio_id = int(selected_db_portfolio.split("(ID: ")[1].split(")")[0])
            
            if st.sidebar.button("Load DB Portfolio"):
                # Load portfolio from database
                portfolio_data = load_portfolio(portfolio_id)
                if portfolio_data:
                    # Convert to Portfolio object
                    st.session_state.portfolio = Portfolio.from_dict(portfolio_data)
                    st.session_state.current_portfolio_name = portfolio_data.get('name', f"DB Portfolio {portfolio_id}")
                    st.sidebar.success(f"Portfolio loaded from database successfully!")
                else:
                    st.sidebar.error("Failed to load portfolio from database.")
        else:
            st.sidebar.info("No portfolios found in the database. Save a portfolio first.")
    except Exception as e:
        st.sidebar.error(f"Error accessing database: {str(e)}")

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
    from custom_pages.pages.allocation import show_allocation_page
    show_allocation_page(st.session_state.portfolio)
elif page == "Compound Growth":
    from custom_pages.pages.compound_growth import show_compound_growth_page
    show_compound_growth_page(st.session_state.portfolio)
elif page == "Fund Comparison":
    from custom_pages.pages.fund_comparison import show_fund_comparison_page
    show_fund_comparison_page()
elif page == "Tax Efficiency":
    from custom_pages.pages.tax_efficiency import show_tax_efficiency_page
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
