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
        st.markdown("""
        Compare how these funds' prices have changed over time. This visualization helps illustrate:
        - How funds in the same category tend to move together over time
        - The effect of market events on different fund categories
        - How funds with lower expense ratios may slightly outperform over long periods
        - The relative price stability of bond funds compared to stock funds
        
        Use the Growth of $10,000 view to see how an initial investment would have grown over time.
        """)
        
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
                    **Note:** This chart shows simulated price data based on realistic market conditions and historical 
                    patterns for each fund category. The simulation accounts for fund-specific characteristics including:
                    
                    • Expense ratios (lower expense ratio funds should slightly outperform over time)
                    • Typical market volatility including bear and bull markets
                    • Category-specific behaviors (bond funds are more stable than stock funds)
                    • Realistic correlations between similar funds
                    
                    While not representing actual historical prices, this simulation provides a realistic illustration 
                    of how index funds with similar objectives typically perform relative to each other over time.
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
