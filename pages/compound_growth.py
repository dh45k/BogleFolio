import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.compound_calculator import calculate_portfolio_growth, calculate_fee_impact

def show_compound_growth_page(portfolio):
    """
    Display the compound growth projection page
    """
    st.header("Compound Growth Projections")
    
    # Investment parameters section
    st.subheader("Investment Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        initial_investment = st.number_input(
            "Initial Investment ($)",
            min_value=0,
            value=portfolio.initial_investment,
            step=1000
        )
    
    with col2:
        monthly_contribution = st.number_input(
            "Monthly Contribution ($)",
            min_value=0,
            value=portfolio.monthly_contribution,
            step=100
        )
    
    with col3:
        years_to_grow = st.number_input(
            "Years to Grow",
            min_value=1,
            max_value=50,
            value=portfolio.years_to_grow,
            step=1
        )
    
    # Update portfolio if parameters have changed
    if (initial_investment != portfolio.initial_investment or
        monthly_contribution != portfolio.monthly_contribution or
        years_to_grow != portfolio.years_to_grow):
        
        portfolio.initial_investment = initial_investment
        portfolio.monthly_contribution = monthly_contribution
        portfolio.years_to_grow = years_to_grow
        
        # Also update account values proportionally if initial investment changed
        if initial_investment != portfolio.initial_investment:
            total_accounts = sum(portfolio.account_values.values())
            if total_accounts > 0:
                ratio = initial_investment / total_accounts
                portfolio.account_values = {k: v * ratio for k, v in portfolio.account_values.items()}
        
        st.success("Investment parameters updated!")
    
    # Expected returns section
    st.subheader("Expected Returns")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        us_return = st.number_input(
            "US Stocks Annual Return (%)",
            min_value=0.0,
            max_value=20.0,
            value=portfolio.expected_return_us,
            step=0.1,
            format="%.1f"
        )
    
    with col2:
        intl_return = st.number_input(
            "International Stocks Annual Return (%)",
            min_value=0.0,
            max_value=20.0,
            value=portfolio.expected_return_intl,
            step=0.1,
            format="%.1f"
        )
    
    with col3:
        bond_return = st.number_input(
            "Bonds Annual Return (%)",
            min_value=0.0,
            max_value=20.0,
            value=portfolio.expected_return_bond,
            step=0.1,
            format="%.1f"
        )
    
    # Update portfolio if returns have changed
    if (us_return != portfolio.expected_return_us or
        intl_return != portfolio.expected_return_intl or
        bond_return != portfolio.expected_return_bond):
        
        portfolio.expected_return_us = us_return
        portfolio.expected_return_intl = intl_return
        portfolio.expected_return_bond = bond_return
        
        st.success("Expected returns updated!")
    
    # Calculate weighted return
    weighted_return = portfolio.get_weighted_return()
    st.metric("Weighted Expected Annual Return", f"{weighted_return:.2f}%")
    
    # Calculate and project growth
    growth_data = calculate_portfolio_growth(portfolio)
    
    # Growth visualization
    st.subheader("Growth Projections")
    
    # Create line chart of growth
    fig = go.Figure()
    
    # Add total growth line
    fig.add_trace(go.Scatter(
        x=growth_data['Year'],
        y=growth_data['Total Balance'],
        mode='lines',
        name='Total Portfolio',
        line=dict(color='rgb(31, 119, 180)', width=4)
    ))
    
    # Add component lines
    fig.add_trace(go.Scatter(
        x=growth_data['Year'],
        y=growth_data['US Stocks'],
        mode='lines',
        name='US Stocks',
        line=dict(color='rgb(255, 127, 14)', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=growth_data['Year'],
        y=growth_data['International Stocks'],
        mode='lines',
        name='International Stocks',
        line=dict(color='rgb(44, 160, 44)', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=growth_data['Year'],
        y=growth_data['Bonds'],
        mode='lines',
        name='Bonds',
        line=dict(color='rgb(214, 39, 40)', width=2)
    ))
    
    # Update layout
    fig.update_layout(
        title='Portfolio Value Over Time',
        xaxis_title='Years',
        yaxis_title='Value ($)',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Format y-axis as currency
    fig.update_yaxes(tickprefix='$', tickformat=',.0f')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Area chart showing contributions vs earnings
    fig_area = go.Figure()
    
    fig_area.add_trace(go.Scatter(
        x=growth_data['Year'],
        y=growth_data['Total Contributions'],
        mode='lines',
        name='Contributions',
        line=dict(width=0),
        stackgroup='one',
        fillcolor='rgba(44, 160, 44, 0.5)'
    ))
    
    fig_area.add_trace(go.Scatter(
        x=growth_data['Year'],
        y=growth_data['Total Earnings'],
        mode='lines',
        name='Earnings',
        line=dict(width=0),
        stackgroup='one',
        fillcolor='rgba(31, 119, 180, 0.5)'
    ))
    
    fig_area.update_layout(
        title='Contributions vs. Earnings Over Time',
        xaxis_title='Years',
        yaxis_title='Value ($)',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Format y-axis as currency
    fig_area.update_yaxes(tickprefix='$', tickformat=',.0f')
    
    st.plotly_chart(fig_area, use_container_width=True)
    
    # Display data table with key years
    st.subheader("Growth Milestones")
    
    # Select key years to show (0, 5, 10, 15, 20, 30, 40, 50 - up to max years)
    key_years = [0, 5, 10, 15, 20, 30, 40, 50]
    key_years = [year for year in key_years if year <= years_to_grow]
    
    # Create milestone dataframe
    milestones = growth_data[growth_data['Year'].isin(key_years)].copy()
    milestones = milestones[['Year', 'Total Balance', 'Total Contributions', 'Total Earnings']]
    
    # Format the currency columns
    milestones['Total Balance'] = milestones['Total Balance'].map('${:,.0f}'.format)
    milestones['Total Contributions'] = milestones['Total Contributions'].map('${:,.0f}'.format)
    milestones['Total Earnings'] = milestones['Total Earnings'].map('${:,.0f}'.format)
    
    st.dataframe(milestones, use_container_width=True)
    
    # Fee impact section
    st.divider()
    st.subheader("Expense Ratio Impact")
    
    # Calculate current weighted expense ratio
    current_expense = portfolio.get_weighted_expense_ratio()
    
    # Allow comparison with lower expense ratio
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Current Weighted Expense Ratio", f"{current_expense:.3%}")
    
    with col2:
        compare_expense = st.number_input(
            "Compare with Expense Ratio (%)",
            min_value=0.0,
            max_value=1.0,
            value=max(current_expense/2, 0.0001),
            step=0.01,
            format="%0.4f"
        )
    
    # Calculate fee impact
    fee_impact = calculate_fee_impact(portfolio, compare_expense)
    
    # Plot fee impact
    fig_fee = go.Figure()
    
    # Add current expense ratio line
    fig_fee.add_trace(go.Scatter(
        x=fee_impact['Year'],
        y=fee_impact[f'Balance (Expense Ratio: {current_expense:.3%})'],
        mode='lines',
        name=f'Current ({current_expense:.3%})',
        line=dict(color='rgb(31, 119, 180)', width=3)
    ))
    
    # Add comparison expense ratio line
    fig_fee.add_trace(go.Scatter(
        x=fee_impact['Year'],
        y=fee_impact[f'Balance (Expense Ratio: {compare_expense:.3%})'],
        mode='lines',
        name=f'Lower ({compare_expense:.3%})',
        line=dict(color='rgb(44, 160, 44)', width=3)
    ))
    
    # Update layout
    fig_fee.update_layout(
        title='Impact of Expense Ratios Over Time',
        xaxis_title='Years',
        yaxis_title='Value ($)',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Format y-axis as currency
    fig_fee.update_yaxes(tickprefix='$', tickformat=',.0f')
    
    st.plotly_chart(fig_fee, use_container_width=True)
    
    # Show total fee impact at end of period
    final_impact = fee_impact.iloc[-1]['Fee Impact']
    current_balance = fee_impact.iloc[-1][f'Balance (Expense Ratio: {current_expense:.3%})']
    st.metric(
        f"Total Fee Savings After {years_to_grow} Years",
        f"${final_impact:,.0f}",
        f"{final_impact / current_balance * 100:.2f}%"
    )
