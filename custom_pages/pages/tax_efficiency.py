import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.tax_efficiency import TaxEfficiencyCalculator
from custom_pages.pages.shared import display_quote, display_boglebot_sidebar

def show_tax_efficiency_page(portfolio):
    """
    Display the tax efficiency page
    """
    # Display a Bogle quote
    display_quote()
    
    # Add the Boglebot chat interface
    display_boglebot_sidebar()
    st.header("Tax-Efficient Fund Placement")
    
    # Create tax efficiency calculator
    tax_calculator = TaxEfficiencyCalculator()
    
    # Account overview
    st.subheader("Current Account Values")
    
    # Show account values in a table
    account_df = pd.DataFrame({
        'Account Type': list(portfolio.account_values.keys()),
        'Value ($)': list(portfolio.account_values.values())
    })
    
    # Check if we have any account values
    if sum(portfolio.account_values.values()) > 0:
        st.dataframe(account_df, use_container_width=True)
        
        # Generate tax-efficient recommendations
        recommendations = tax_calculator.generate_recommendations(portfolio)
        
        if not recommendations.empty:
            st.subheader("Recommended Fund Placement")
            
            # Format the amount column
            recommendations['Amount'] = recommendations['Amount'].map('${:,.0f}'.format)
            
            # Display recommendations
            st.dataframe(
                recommendations[['Fund', 'Fund Type', 'Account', 'Amount', 'Percent of Portfolio']],
                use_container_width=True
            )
            
            # Create a visualization of the recommendations
            fig = px.bar(
                recommendations,
                x='Account',
                y='Percent of Portfolio',
                color='Fund Type',
                title='Tax-Efficient Fund Placement',
                text='Fund',
                hover_data=['Amount']
            )
            
            # Update layout
            fig.update_layout(
                xaxis_title='Account Type',
                yaxis_title='Allocation (%)',
                barmode='stack'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Unable to generate recommendations. Please ensure you have funds and accounts configured.")
    else:
        st.warning("Please set account values on the Portfolio Allocation page before generating tax-efficiency recommendations.")
    
    # Display educational information about tax efficiency
    st.divider()
    st.subheader("Tax Efficiency Principles")
    
    # Get tax efficiency explanation
    explanation = tax_calculator.get_tax_efficiency_explanation()
    
    for item in explanation["explanations"]:
        st.markdown(f"#### {item['principle']}")
        st.markdown(item['description'])
    
    # Detailed tax-efficiency explanation
    st.divider()
    st.subheader("Tax Efficiency Details")
    
    st.markdown("""
    ### Understanding Tax Efficiency
    
    Tax efficiency is about placing your investments in the right types of accounts to minimize taxes. Here's a more detailed explanation of how to optimize your portfolio tax-efficiency:
    
    #### Account Types and Tax Treatment
    
    1. **Tax-Advantaged Accounts**
       - **Traditional 401(k)/IRA**: Contributions are tax-deductible, growth is tax-deferred, withdrawals are taxed as ordinary income
       - **Roth 401(k)/IRA**: Contributions are after-tax, growth and qualified withdrawals are tax-free
       - **HSA**: Triple tax advantage - tax-deductible contributions, tax-free growth, and tax-free withdrawals for qualified medical expenses
    
    2. **Taxable Accounts**
       - Growth is subject to capital gains tax (short-term or long-term)
       - Dividends are taxed annually (qualified or ordinary)
       - Interest is taxed as ordinary income
    
    #### Fund Characteristics and Tax Efficiency
    
    | Fund Type | Tax Efficiency | Best Account Placement |
    |-----------|---------------|------------------------|
    | US Total Market Funds | High | Taxable |
    | International Funds | Medium | Taxable (for foreign tax credit) or Tax-advantaged |
    | REITs | Low | Tax-advantaged |
    | Corporate Bonds | Low | Tax-advantaged |
    | Treasury Bonds | Medium | Tax-advantaged or Taxable |
    | TIPS | Low | Tax-advantaged |
    | High-Yield Bonds | Low | Tax-advantaged |
    
    #### Implementation Strategy
    
    1. **First Priority**: Fill tax-advantaged accounts with tax-inefficient assets
    2. **Second Priority**: Place remaining tax-inefficient assets in other tax-advantaged accounts
    3. **Third Priority**: Place tax-efficient assets in taxable accounts
    
    #### Additional Considerations
    
    - **State taxes** may impact optimal placement
    - **Investment time horizon** affects the benefits of tax-efficient placement
    - **Rebalancing needs** should be considered when deciding placement
    - **Required Minimum Distributions (RMDs)** may affect long-term tax planning
    
    By following these principles, you can significantly reduce the tax drag on your portfolio and improve your after-tax returns.
    
    > *"Invest as efficiently as you can, using low-cost funds that can be bought and held for a lifetime."* - Jack Bogle
    """)
