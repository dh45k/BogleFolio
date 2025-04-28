import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.fund_data import get_fund_data, get_historical_prices

def show_fund_comparison_page():
    """
    Display the fund comparison page
    """
    st.header("Fund Comparison")
    
    # Get fund data
    fund_data = get_fund_data()
    
    # Fund category and provider filters
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Filter by category
        categories = sorted(fund_data['Category'].unique())
        selected_categories = st.multiselect(
            "Filter by Fund Category",
            options=categories,
            default=["US Total Market", "International Developed", "US Total Bond"]
        )
    
    with col2:
        # Filter by provider
        providers = sorted(fund_data['Provider'].unique())
        selected_providers = st.multiselect(
            "Filter by Provider",
            options=providers,
            default=providers
        )
    
    # Apply filters
    if selected_categories and selected_providers:
        filtered_data = fund_data[
            fund_data['Category'].isin(selected_categories) &
            fund_data['Provider'].isin(selected_providers)
        ]
    elif selected_categories:
        filtered_data = fund_data[fund_data['Category'].isin(selected_categories)]
    elif selected_providers:
        filtered_data = fund_data[fund_data['Provider'].isin(selected_providers)]
    else:
        filtered_data = fund_data
    
    # Display filtered data
    if not filtered_data.empty:
        # Sort by expense ratio
        filtered_data = filtered_data.sort_values('Expense Ratio')
        
        # Format expense ratio for display
        display_data = filtered_data.copy()
        display_data['Expense Ratio'] = display_data['Expense Ratio'].apply(lambda x: f"{x:.4%}")
        
        st.dataframe(
            display_data[['Ticker', 'Fund Name', 'Provider', 'Category', 'Expense Ratio']],
            use_container_width=True
        )
        
        # Visualize expense ratios by category
        st.subheader("Expense Ratio Comparison")
        
        # Group by category and provider for box plot
        fig = px.box(
            filtered_data,
            x='Category',
            y='Expense Ratio',
            color='Provider',
            title='Expense Ratios by Fund Category and Provider',
            points='all',
            hover_data=['Ticker', 'Fund Name']
        )
        
        # Format y-axis as percentage
        fig.update_yaxes(tickformat='.3%')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Bar chart comparing expense ratios directly
        st.subheader("Fund Expense Ratio Comparison")
        
        # Select fund type to compare
        fund_type = st.selectbox(
            "Select Fund Category to Compare",
            options=selected_categories if selected_categories else categories
        )
        
        # Filter by selected fund type
        type_data = filtered_data[filtered_data['Category'] == fund_type].copy()
        type_data = type_data.sort_values('Expense Ratio')
        
        # Create bar chart
        fig_bar = px.bar(
            type_data,
            x='Ticker',
            y='Expense Ratio',
            color='Provider',
            title=f'Expense Ratio Comparison for {fund_type} Funds',
            hover_data=['Fund Name'],
            text_auto='.3%'
        )
        
        # Format y-axis as percentage
        fig_bar.update_yaxes(tickformat='.3%')
        
        # Update layout
        fig_bar.update_layout(
            xaxis_title='Fund Ticker',
            yaxis_title='Expense Ratio'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Cost comparison over time
        st.subheader("Cost Comparison Over Time")
        
        # Select funds to compare
        col1, col2 = st.columns([1, 1])
        
        with col1:
            investment_amount = st.number_input(
                "Investment Amount ($)",
                min_value=10000,
                value=100000,
                step=10000
            )
        
        with col2:
            comparison_years = st.slider(
                "Years to Compare",
                min_value=1,
                max_value=30,
                value=10
            )
        
        # Allow selection of funds to compare
        selected_funds = st.multiselect(
            "Select Funds to Compare",
            options=type_data['Ticker'].tolist(),
            default=type_data['Ticker'].tolist()[:3] if len(type_data) >= 3 else type_data['Ticker'].tolist()
        )
        
        if selected_funds:
            # Calculate cost over time
            funds_to_compare = type_data[type_data['Ticker'].isin(selected_funds)]
            
            # Create comparison chart
            fig_cost = go.Figure()
            
            for _, fund in funds_to_compare.iterrows():
                # Calculate cost over years
                years = list(range(comparison_years + 1))
                costs = [investment_amount * fund['Expense Ratio'] * year for year in years]
                cumulative_costs = [sum(costs[:i+1]) for i in range(len(costs))]
                
                # Add line to chart
                fig_cost.add_trace(go.Scatter(
                    x=years,
                    y=cumulative_costs,
                    mode='lines+markers',
                    name=f"{fund['Ticker']} ({fund['Expense Ratio']:.3%})",
                    hovertemplate='Year: %{x}<br>Cumulative Cost: $%{y:,.2f}'
                ))
            
            # Update layout
            fig_cost.update_layout(
                title=f'Cumulative Cost Comparison for ${investment_amount:,} Investment',
                xaxis_title='Years',
                yaxis_title='Cumulative Cost ($)',
                hovermode='x unified'
            )
            
            # Format y-axis as currency
            fig_cost.update_yaxes(tickprefix='$', tickformat=',.0f')
            
            st.plotly_chart(fig_cost, use_container_width=True)
            
            # Calculate final cost difference but don't display the problematic text
            if len(selected_funds) > 1:
                final_costs = {}
                
                for _, fund in funds_to_compare.iterrows():
                    final_cost = investment_amount * fund['Expense Ratio'] * comparison_years
                    final_costs[fund['Ticker']] = final_cost
                    
        # Price comparison over time chart
        st.subheader("Fund Price Comparison")
        
        # Allow selection of funds to compare
        st.markdown("Compare how these funds' prices have changed over time.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            history_years = st.slider(
                "Years of Price History",
                min_value=1,
                max_value=10,
                value=5
            )
        
        with col2:
            price_display = st.radio(
                "Display as",
                options=["Actual Price", "Growth of $10,000"],
                index=0
            )
        
        # Generate and display the price chart if there are selected funds
        if selected_funds:
            # Get historical price data
            price_data = get_historical_prices(selected_funds, years=history_years)
            
            if not price_data.empty:
                # Create price comparison chart
                fig_price = go.Figure()
                
                # Handle either actual price or growth format
                if price_display == "Actual Price":
                    # Plot actual prices
                    for ticker in selected_funds:
                        if ticker in price_data.columns:
                            fund_info = fund_data[fund_data['Ticker'] == ticker].iloc[0]
                            fig_price.add_trace(go.Scatter(
                                x=price_data['Date'],
                                y=price_data[ticker],
                                mode='lines',
                                name=f"{ticker} - {fund_info['Provider']}",
                                hovertemplate='Date: %{x|%b %Y}<br>Price: $%{y:.2f}'
                            ))
                    
                    # Update layout
                    fig_price.update_layout(
                        title=f'Fund Price Comparison - {fund_type} Funds',
                        xaxis_title='Date',
                        yaxis_title='Price ($)',
                        hovermode='x unified'
                    )
                    
                    # Format y-axis as currency
                    fig_price.update_yaxes(tickprefix='$', tickformat=',.2f')
                    
                else:  # Growth of $10,000
                    # Calculate growth of $10,000 for each fund
                    initial_investment = 10000
                    
                    for ticker in selected_funds:
                        if ticker in price_data.columns:
                            # Calculate normalized series
                            first_price = price_data[ticker].iloc[0]
                            growth_series = price_data[ticker] / first_price * initial_investment
                            
                            # Add to chart
                            fund_info = fund_data[fund_data['Ticker'] == ticker].iloc[0]
                            fig_price.add_trace(go.Scatter(
                                x=price_data['Date'],
                                y=growth_series,
                                mode='lines',
                                name=f"{ticker} - {fund_info['Provider']}",
                                hovertemplate='Date: %{x|%b %Y}<br>Value: $%{y:.2f}'
                            ))
                    
                    # Update layout
                    fig_price.update_layout(
                        title=f'Growth of $10,000 - {fund_type} Funds',
                        xaxis_title='Date',
                        yaxis_title='Value ($)',
                        hovermode='x unified'
                    )
                    
                    # Format y-axis as currency
                    fig_price.update_yaxes(tickprefix='$', tickformat=',.0f')
                
                # Show the chart
                st.plotly_chart(fig_price, use_container_width=True)
                
                # Add explanatory note
                st.caption("""
                    Note: This chart shows estimated price movements based on typical market behavior for each fund category.
                    Different funds in the same category may show slightly different performance due to tracking differences, 
                    securities lending income, and other factors.
                """)
                
                # Combined price and fee chart
                st.subheader("Combined Price and Fee Impact")
                
                # Only create this visualization if we have funds to compare
                if len(selected_funds) > 0:
                    # Create a figure with secondary y-axis
                    fig_combined = go.Figure()
                    
                    # Calculate estimated returns after fees over time
                    investment_amount = 10000  # Start with $10,000
                    
                    for ticker in selected_funds:
                        if ticker in price_data.columns:
                            # Get fund info
                            fund_info = fund_data[fund_data['Ticker'] == ticker].iloc[0]
                            expense_ratio = fund_info['Expense Ratio']
                            
                            # Calculate growth adjusted for fees
                            first_price = price_data[ticker].iloc[0]
                            growth_series = []
                            
                            # Get all values except the date column
                            prices = price_data[ticker].values
                            dates = price_data['Date'].values
                            
                            value = investment_amount
                            values_after_fees = []
                            
                            # Calculate value for each time period, adjusted for fees
                            for i in range(len(prices)):
                                if i > 0:
                                    # Calculate raw return for this period
                                    period_return = prices[i] / prices[i-1] - 1
                                    
                                    # Apply monthly fee (annual fee divided by 12)
                                    monthly_fee = expense_ratio / 12
                                    
                                    # Adjust return for fees
                                    net_return = period_return - monthly_fee
                                    
                                    # Update value
                                    value = value * (1 + net_return)
                                
                                values_after_fees.append(value)
                            
                            # Add after-fee growth line
                            fig_combined.add_trace(go.Scatter(
                                x=dates,
                                y=values_after_fees,
                                mode='lines',
                                name=f"{ticker} (After {expense_ratio:.3%} Fees)",
                                hovertemplate='Date: %{x|%b %Y}<br>Value After Fees: $%{y:.2f}'
                            ))
                            
                            # Also calculate total fees paid
                            cumulative_fees = []
                            fee_total = 0
                            
                            for i in range(len(prices)):
                                if i > 0:
                                    # Calculate period fee based on value
                                    period_fee = values_after_fees[i-1] * (expense_ratio / 12)
                                    fee_total += period_fee
                                
                                cumulative_fees.append(fee_total)
                            
                            # Add cumulative fees line with secondary y-axis
                            fig_combined.add_trace(go.Scatter(
                                x=dates,
                                y=cumulative_fees,
                                mode='lines',
                                name=f"{ticker} (Fees Paid)",
                                line=dict(dash='dash'),
                                hovertemplate='Date: %{x|%b %Y}<br>Cumulative Fees: $%{y:.2f}',
                                yaxis="y2"
                            ))
                    
                    # Update layout with dual y-axes
                    fig_combined.update_layout(
                        title=f'Growth of $10,000 with Fee Impact - {fund_type} Funds',
                        xaxis_title='Date',
                        yaxis_title='Value After Fees ($)',
                        yaxis2=dict(
                            title='Cumulative Fees Paid ($)',
                            overlaying='y',
                            side='right',
                            rangemode='tozero'
                        ),
                        hovermode='x unified',
                        legend=dict(
                            orientation="h",
                            y=-0.2
                        )
                    )
                    
                    # Format y-axes as currency
                    fig_combined.update_yaxes(tickprefix='$', tickformat=',.0f')
                    
                    # Show the chart
                    st.plotly_chart(fig_combined, use_container_width=True)
                    
                    # Add explanatory note for the combined chart
                    st.caption("""
                        This chart illustrates how expense ratios impact actual investment returns over time. 
                        Solid lines show investment growth after fees, while dashed lines show the cumulative fees paid 
                        (displayed on the right axis). Even small fee differences can have a significant impact 
                        on long-term performance.
                    """)
            else:
                st.warning("Unable to generate price comparison chart for the selected funds.")
    else:
        st.warning("No funds match the selected filters. Please adjust your criteria.")
    
    # Educational section on expense ratios
    st.divider()
    st.subheader("Understanding Expense Ratios")
    
    st.markdown("""
    ### Why Expense Ratios Matter
    
    Expense ratios represent the annual fee that funds charge their shareholders. It's expressed as a percentage of assets under management.
    
    #### Impact on Long-Term Returns
    
    Even small differences in expense ratios can have a significant impact on your investment returns over time due to compounding:
    
    - A 0.1% difference in expense ratio on a $100,000 investment over 30 years could mean approximately $30,000 in lost returns.
    - Lower expense ratios mean more of your money stays invested and working for you.
    
    #### Expense Ratio Considerations
    
    - **Index funds** typically have much lower expense ratios than actively managed funds.
    - **ETFs** often have lower expense ratios than mutual funds with similar investment objectives.
    - Some brokerages offer proprietary funds with zero or near-zero expense ratios.
    - Consider expense ratios alongside other factors like tracking error and tax efficiency.
    
    Following the Bogleheads philosophy, keeping costs low is one of the most reliable ways to improve your investment returns over time.
    
    > *"Time is your friend; impulse is your enemy."* - Jack Bogle
    
    > *"Stay the course!"* - Jack Bogle
    """)
