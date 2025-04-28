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
        
        # Set up interface for allocation inputs
        st.write("Adjust allocation using sliders or enter percentages directly:")
        
        # Function to initialize session state for synchronized values if not already present
        def init_synced_value(key, default_value):
            if f"{key}_value" not in st.session_state:
                st.session_state[f"{key}_value"] = default_value
        
        # Initialize session state for each allocation type
        init_synced_value("us_stocks", portfolio.us_stock_allocation)
        init_synced_value("intl_stocks", portfolio.international_stock_allocation)
        init_synced_value("bonds", portfolio.bond_allocation)
        
        # Create callbacks to sync the values
        def update_value(key):
            def callback():
                # Update the synced value whenever either input changes
                input_value = st.session_state.get(f"{key}_input", 0)
                slider_value = st.session_state.get(f"{key}_slider", 0)
                # Use the most recently changed value
                st.session_state[f"{key}_value"] = input_value
            return callback
        
        # Helper function to create allocation input row with label, slider and number input
        def allocation_input_row(label, key):
            col_label, col_slider, col_input = st.columns([2, 4, 1])
            
            with col_label:
                st.write(f"**{label}**")
            
            # Get the current synced value
            current_value = st.session_state[f"{key}_value"]
            
            with col_slider:
                st.slider(
                    f"###{label} Slider", 
                    min_value=0, max_value=100, 
                    value=current_value,
                    step=1,
                    key=f"{key}_slider",
                    on_change=update_value(key),
                    label_visibility="collapsed"
                )
            
            with col_input:
                st.number_input(
                    f"###{label} Input", 
                    min_value=0, max_value=100, 
                    value=current_value,
                    step=1,
                    key=f"{key}_input",
                    on_change=update_value(key),
                    label_visibility="collapsed"
                )
            
            # Return the synced value
            return st.session_state[f"{key}_value"]
        
        # Display allocation inputs using our new approach
        us_stocks = allocation_input_row("US Stocks (%)", "us_stocks")
        international_stocks = allocation_input_row("International Stocks (%)", "intl_stocks")
        bonds = allocation_input_row("Bonds (%)", "bonds")
        
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
    
    # Add a helpful note at the bottom
    st.divider()
    st.info("Visit the **Financial Literacy** page for more information about Jack Bogle's investment philosophy and resources for Bogleheads investors.")
