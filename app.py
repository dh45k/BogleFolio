import streamlit as st
import os
import json
import base64
from utils.portfolio import Portfolio

# Set page config
st.set_page_config(
    page_title="Boglehead Portfolio Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load local CSS file
def load_css(css_file):
    with open(css_file, "r") as f:
        css = f.read()
    return css

# Load custom CSS
css = load_css("assets/style.css")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Function to display SVG image
def render_svg(svg_file):
    with open(svg_file, "r") as f:
        svg = f.read()
    return svg

# Initialize session state for portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = Portfolio()

if 'portfolios' not in st.session_state:
    st.session_state.portfolios = {}

if 'current_portfolio_name' not in st.session_state:
    st.session_state.current_portfolio_name = "Default Portfolio"
    
if 'page' not in st.session_state:
    st.session_state.page = "Portfolio Allocation"

# Create header with logo and title
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown(render_svg("assets/logo.svg"), unsafe_allow_html=True)
with col_title:
    st.markdown('<h1 class="header-title">Boglehead 3-Fund Portfolio Optimizer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Simplify investing with diversified, low-cost index funds</p>', unsafe_allow_html=True)

# Create tabs for navigation with custom styling - sticky at the top
st.markdown('<div class="nav-container sticky-nav">', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns(6)

# CSS for navigation buttons with icons
nav_styles = """
<style>
    /* Sticky navigation container */
    .sticky-nav {
        position: sticky;
        top: 0;
        z-index: 1000;
        background-color: #fff;
        padding: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0 -2rem;  /* Compensate for container padding */
        padding: 10px 2rem;  /* Add padding to match container */
        margin-bottom: 20px;
        border-bottom: 1px solid #eee;
    }
    
    /* Space above sticky nav to prevent content from being hidden */
    .main .block-container::before {
        content: "";
        display: block;
        height: 3rem;
    }

    .nav-container button {
        background-color: #f8f9fa;
        color: #333;
        border: none;
        padding: 0.5rem;
        border-radius: 4px;
        font-weight: 500;
        transition: all 0.2s;
        border: 1px solid #eee;
    }
    .nav-container button:hover {
        background-color: #e9f7ef;
        color: #1E5631;
        border: 1px solid #1E5631;
    }
    .nav-icon {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 24px;
        width: 24px;
        margin: 0 auto;
    }
    .nav-icon svg {
        width: 24px;
        height: 24px;
    }
    .st-emotion-cache-7ym5gk {
        display: inline-block;
    }
    .nav-container svg path {
        transition: fill 0.3s, stroke 0.3s;
    }
    .nav-container button:hover svg path {
        stroke: #1E5631;
    }
    
    /* Add padding to the top of the content to prevent it from being hidden behind sticky nav */
    .main .block-container {
        padding-top: 20px;
    }
</style>
"""
st.markdown(nav_styles, unsafe_allow_html=True)

# Define active class for current page with icon
def nav_button(label, page_name, container, icon_path=None):
    active_class = "active" if st.session_state.page == page_name else ""
    
    with container:
        # Determine the button style based on whether it's active
        button_style = """
            background-color: #1E5631;
            color: white;
            border: 1px solid #1E5631;
        """ if st.session_state.page == page_name else ""
        
        # Create a layout for icon and text
        if icon_path:
            # Create a custom HTML button with icon and text
            icon_svg = render_svg(icon_path)
            button_id = f"nav_btn_{page_name.replace(' ', '_')}"
            
            # Apply active styling directly
            button_html = f"""
            <button 
                id="{button_id}" 
                style="
                    display: flex;
                    width: 100%;
                    align-items: center;
                    padding: 8px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-weight: 500;
                    transition: all 0.2s;
                    border: 1px solid #eee;
                    background-color: {('#1E5631' if st.session_state.page == page_name else '#f8f9fa')};
                    color: {('white' if st.session_state.page == page_name else '#333')};
                "
                onclick="
                    window.location.href = window.location.pathname + '?page={page_name}';
                "
            >
                <div style="width: 24px; margin-right: 8px;">{icon_svg}</div>
                <div style="flex-grow: 1; text-align: left;">{label}</div>
            </button>
            """
            
            # Add custom script to handle the click (this is needed for button functionality)
            st.markdown(f"""
            <div>{button_html}</div>
            <script>
                document.getElementById("{button_id}").addEventListener("click", function() {{
                    // Submit a form to trigger page reload with new parameter
                    const form = document.createElement('form');
                    form.method = 'get';
                    form.action = window.location.pathname;
                    
                    const pageInput = document.createElement('input');
                    pageInput.type = 'hidden';
                    pageInput.name = 'page';
                    pageInput.value = '{page_name}';
                    form.appendChild(pageInput);
                    
                    document.body.appendChild(form);
                    form.submit();
                }});
            </script>
            """, unsafe_allow_html=True)
            
            # Also add an invisible button for Streamlit's native navigation
            # This ensures the session state is properly updated even if JavaScript fails
            st.markdown(f'<div style="display:none">', unsafe_allow_html=True)
            if st.button("", key=f"nav_{page_name}", help=f"Navigate to {label} page"):
                st.session_state['page'] = page_name
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
                
        else:
            # Fallback to regular button if no icon
            if st.button(label, key=f"nav_{page_name}", use_container_width=True, 
                    help=f"Navigate to {label} page"):
                st.session_state['page'] = page_name
                st.rerun()

nav_button("Portfolio Allocation", "Portfolio Allocation", col1, "assets/portfolio_allocation.svg")
nav_button("Compound Growth", "Compound Growth", col2, "assets/compound_growth.svg")
nav_button("Fund Comparison", "Fund Comparison", col3, "assets/fund_comparison.svg")
nav_button("Tax Efficiency", "Tax Efficiency", col4, "assets/tax_efficiency.svg")
nav_button("Monte Carlo", "Monte Carlo Simulation", col5, "assets/monte_carlo.svg")
nav_button("Financial Literacy", "Financial Literacy", col6, "assets/financial_literacy.svg")

st.markdown('</div>', unsafe_allow_html=True)

# Add a subtle divider
st.markdown('<hr style="height:2px;border:none;color:#f0f0f0;background-color:#f0f0f0;margin-bottom:24px;">', unsafe_allow_html=True)

# Hide default Streamlit menu, footer, completely hide the sidebar, and all header controls
hide_elements_style = """
        <style>
        /* Hide main menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Hide sidebar completely */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Adjust main content container */
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1200px;
        }
        
        /* Hide ALL header elements - this will remove the '>' button */
        header {
            background-color: transparent !important;
        }
        
        header > div:first-child {
            display: none !important;
        }
        
        /* Hide ALL sidebar control elements */
        div[data-testid="collapsedControl"] {
            display: none !important;
        }
        
        /* Additional specific selectors for the hamburger/sidebar button */
        button[kind="headerNoPadding"] {
            display: none !important;
        }
        
        header button[data-testid="baseButton-headerNoPadding"] {
            display: none !important;
        }
        
        /* Emotion cache classes that might contain the button */
        .st-emotion-cache-1dp5vir {
            display: none !important;
        }
        
        .st-emotion-cache-jnd7a {
            display: none !important;
        }
        
        /* More aggressive approach to hide all header buttons */
        header button {
            display: none !important;
        }
        </style>
        
        <script>
        // JavaScript to remove the button after page loads
        document.addEventListener('DOMContentLoaded', function() {
            // Hide any sidebar toggle buttons that might appear
            const sidebarButtons = document.querySelectorAll('[data-testid="collapsedControl"]');
            sidebarButtons.forEach(button => {
                button.style.display = 'none';
            });
            
            // Also target header buttons
            const headerButtons = document.querySelectorAll('header button');
            headerButtons.forEach(button => {
                button.style.display = 'none';
            });
        });
        </script>
        """
st.markdown(hide_elements_style, unsafe_allow_html=True)

# Hide sidebar navigation - now only using top navigation
# But still keep track of the current page in session state
page_options = ["Portfolio Allocation", "Compound Growth", "Fund Comparison", "Tax Efficiency", "Monte Carlo Simulation", "Financial Literacy"]
page = st.session_state.page

# Portfolio management in sidebar with improved styling
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown('<hr style="margin: 30px 0 20px 0; border-color: #f0f0f0;">', unsafe_allow_html=True)
st.sidebar.markdown('<h2 style="color:#1E5631; font-size:1.5rem; margin-bottom:15px;">Portfolio Management</h2>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Save portfolio
portfolio_name = st.sidebar.text_input("Portfolio Name:", value=st.session_state.current_portfolio_name)

# Update portfolio name
st.session_state.portfolio.name = portfolio_name

# Storage options
storage_option = st.sidebar.radio("Storage:", ["Local", "Database"], horizontal=True)

if st.sidebar.button("Save Portfolio"):
    # Always save to local memory
    st.session_state.portfolios[portfolio_name] = st.session_state.portfolio.to_dict()
    st.session_state.current_portfolio_name = portfolio_name
    
    # If database option selected, also save to database
    if storage_option == "Database":
        try:
            # Use the save_to_db method from the Portfolio class
            portfolio_id = st.session_state.portfolio.save_to_db()
            if portfolio_id:
                st.session_state.portfolio.id = portfolio_id
                st.sidebar.success(f"Portfolio '{portfolio_name}' saved to database (ID: {portfolio_id})!")
            else:
                st.sidebar.error("Error saving to database. See server logs for details.")
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
        # Get list of portfolios using class method
        db_portfolios = Portfolio.get_user_portfolios()
        
        if db_portfolios:
            portfolio_options = [f"{p['name']} (ID: {p['id']})" for p in db_portfolios]
            selected_db_portfolio = st.sidebar.selectbox(
                "Select Database Portfolio:",
                options=portfolio_options
            )
            
            # Extract the ID from the selection
            portfolio_id = int(selected_db_portfolio.split("(ID: ")[1].split(")")[0])
            
            if st.sidebar.button("Load DB Portfolio"):
                # Create a new portfolio instance and load from the database
                new_portfolio = Portfolio()
                success = new_portfolio.load_from_db(portfolio_id)
                
                if success:
                    # Update the current portfolio in session state
                    st.session_state.portfolio = new_portfolio
                    st.session_state.current_portfolio_name = new_portfolio.name
                    
                    # Also save to local portfolios for offline access
                    st.session_state.portfolios[new_portfolio.name] = new_portfolio.to_dict()
                    
                    st.sidebar.success(f"Portfolio '{new_portfolio.name}' (ID: {portfolio_id}) loaded from database successfully!")
                else:
                    st.sidebar.error("Failed to load portfolio from database. See server logs for details.")
        else:
            st.sidebar.info("No portfolios found in the database. Save a portfolio first.")
    except Exception as e:
        import traceback
        print(f"Error loading from database: {e}")
        print(traceback.format_exc())
        st.sidebar.error(f"Error accessing database: {str(e)}")

# Export/Import portfolios with styled section
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown('<hr style="margin: 30px 0 20px 0; border-color: #f0f0f0;">', unsafe_allow_html=True)
st.sidebar.markdown('<h2 style="color:#1E5631; font-size:1.5rem; margin-bottom:15px;">Export/Import</h2>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="font-size:0.9rem; color:#666; margin-bottom:15px;">Save your portfolios as JSON files or import previously saved portfolios.</p>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

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
elif page == "Monte Carlo Simulation":
    from custom_pages.pages.monte_carlo import show_monte_carlo_page
    show_monte_carlo_page(st.session_state.portfolio)
elif page == "Financial Literacy":
    from custom_pages.pages.financial_literacy import show_financial_literacy_page
    show_financial_literacy_page()

# Footer with styled content
st.markdown('<div class="footer-container">', unsafe_allow_html=True)
st.markdown('<hr style="margin: 30px 0; border-color: #f0f0f0;">', unsafe_allow_html=True)

# Create columns for the footer
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<h3 class="footer-title">About This Tool</h3>', unsafe_allow_html=True)
    st.markdown('''
    <div class="footer-content">
        <p style="margin-bottom:15px; line-height:1.5;">This tool is designed for Bogleheads to optimize their 3-fund portfolios. It helps visualize asset allocation, 
        project growth over time, compare fund expenses, optimize tax efficiency across different account types,
        and analyze retirement readiness through Monte Carlo simulations.</p>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown('<h3 class="footer-title">Important Information</h3>', unsafe_allow_html=True)
    st.markdown('''
    <div class="footer-content">
        <div style="background-color:#f8f9fa; border-left:4px solid #1E5631; padding:15px; margin-bottom:20px; border-radius:0 4px 4px 0;">
            <p style="margin-bottom:10px; font-weight:500;">DISCLAIMER:</p>
            <p style="margin-bottom:10px; font-size:0.9rem; line-height:1.5;">This tool and content are for educational and information purposes only. 
            The information provided is not financial or tax advice. Please consult with qualified professionals 
            before making investment decisions.</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
