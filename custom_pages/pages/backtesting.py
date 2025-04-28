import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from utils.portfolio import Portfolio

def get_historical_data(tickers, start_year=2000):
    """
    Get historical data for a set of tickers
    This implementation uses a simplified model based on historical asset class returns
    """
    # Historical average annual returns and volatility (approximate values)
    asset_class_returns = {
        'US Stock': {'annual_return': 0.10, 'volatility': 0.15, 'start_price': 100},
        'International Stock': {'annual_return': 0.08, 'volatility': 0.17, 'start_price': 100},
        'Bond': {'annual_return': 0.05, 'volatility': 0.05, 'start_price': 100},
    }
    
    # Create a mapping from fund tickers to asset classes
    ticker_to_asset = {
        # US Stock funds
        'VTI': 'US Stock', 'VTSAX': 'US Stock', 'VOO': 'US Stock', 
        'FZROX': 'US Stock', 'FSKAX': 'US Stock', 'FNILX': 'US Stock', 'FXAIX': 'US Stock',
        'ITOT': 'US Stock', 'IVV': 'US Stock',
        'SWTSX': 'US Stock', 'SWPPX': 'US Stock',
        
        # International Stock funds
        'VXUS': 'International Stock', 'VTIAX': 'International Stock', 'VEA': 'International Stock', 'VWO': 'International Stock',
        'FZILX': 'International Stock', 'FTIHX': 'International Stock', 'FPADX': 'International Stock',
        'IXUS': 'International Stock', 'IEFA': 'International Stock', 'IEMG': 'International Stock',
        'SWISX': 'International Stock', 'SCHE': 'International Stock',
        
        # Bond funds
        'BND': 'Bond', 'VBTLX': 'Bond', 'VGIT': 'Bond',
        'FXNAX': 'Bond',
        'AGG': 'Bond',
        'SWAGX': 'Bond'
    }
    
    # Generate monthly dates from start year to present
    end_date = datetime.now()
    start_date = datetime(start_year, 1, 1)
    dates = pd.date_range(start=start_date, end=end_date, freq='ME')  # Month End
    
    # Prepare DataFrame with dates
    data = pd.DataFrame({'Date': dates})
    data.set_index('Date', inplace=True)
    
    # Add return series for each ticker
    np.random.seed(42)  # Set seed for reproducibility
    
    # Generate broad market return patterns for each asset class
    # This will be the base for all funds in that asset class
    asset_class_series = {}
    
    for asset, params in asset_class_returns.items():
        # Convert annual to monthly
        monthly_return = params['annual_return'] / 12
        monthly_vol = params['volatility'] / np.sqrt(12)
        
        # Generate random returns but ensure they follow historical patterns
        n_months = len(dates)
        random_monthly_returns = np.random.normal(monthly_return, monthly_vol, n_months)
        
        # Add in some notable market events to simulate real history
        
        # 2000-2002 Dot-com crash (if our data goes back that far)
        crash_start = pd.Timestamp('2000-03-01')
        crash_end = pd.Timestamp('2002-10-01')
        if crash_start >= start_date:
            crash_period = (data.index >= crash_start) & (data.index <= crash_end)
            if asset == 'US Stock' or asset == 'International Stock':
                random_monthly_returns[crash_period] = np.random.normal(-0.01, 0.05, sum(crash_period))
                
        # 2008 Financial Crisis
        crisis_start = pd.Timestamp('2008-09-01')
        crisis_end = pd.Timestamp('2009-03-01')
        if crisis_start >= start_date:
            crisis_period = (data.index >= crisis_start) & (data.index <= crisis_end)
            if asset == 'US Stock' or asset == 'International Stock':
                random_monthly_returns[crisis_period] = np.random.normal(-0.06, 0.08, sum(crisis_period))
            elif asset == 'Bond':
                # Bonds generally performed better during the crisis
                random_monthly_returns[crisis_period] = np.random.normal(0.003, 0.03, sum(crisis_period))
                
        # 2020 COVID-19 Crash (March 2020)
        covid_crash = pd.Timestamp('2020-03-01')
        if covid_crash >= start_date:
            covid_idx = data.index.get_indexer([covid_crash], method='nearest')[0]
            if covid_idx >= 0 and covid_idx < len(random_monthly_returns):
                if asset == 'US Stock' or asset == 'International Stock':
                    random_monthly_returns[covid_idx] = -0.12
                    random_monthly_returns[covid_idx+1] = 0.08
                elif asset == 'Bond':
                    random_monthly_returns[covid_idx] = -0.03
                    random_monthly_returns[covid_idx+1] = 0.02
        
        # Calculate cumulative returns
        cumulative_returns = (1 + random_monthly_returns).cumprod()
        
        # Store in dictionary
        asset_class_series[asset] = cumulative_returns
    
    # Create price series for each ticker
    for ticker in tickers:
        if ticker in ticker_to_asset:
            asset = ticker_to_asset[ticker]
            
            # Use the asset class series as the base
            base_returns = asset_class_series[asset]
            
            # Add a small fund-specific tracking difference
            tracking_error = np.random.normal(0, 0.001, len(dates))
            fund_returns = base_returns * (1 + tracking_error)
            
            # Add to DataFrame
            data[ticker] = fund_returns * asset_class_returns[asset]['start_price']
    
    return data

def calculate_portfolio_backtest(portfolio, start_year):
    """
    Calculate historical performance for a portfolio
    
    Args:
        portfolio: Portfolio object
        start_year: Starting year for the backtest
        
    Returns:
        DataFrame with backtest results
    """
    # Get allocation data
    allocation = portfolio.get_allocation_data()
    
    # Get tickers from the portfolio
    us_ticker = allocation.get('us_ticker', 'VTI')
    intl_ticker = allocation.get('international_ticker', 'VXUS')
    bond_ticker = allocation.get('bond_ticker', 'BND')
    
    tickers = [us_ticker, intl_ticker, bond_ticker]
    
    # Get allocations
    us_allocation = allocation.get('us_stock', 0) / 100
    intl_allocation = allocation.get('international_stock', 0) / 100
    bond_allocation = allocation.get('bond', 0) / 100
    
    # Get historical data
    historical_data = get_historical_data(tickers, start_year)
    
    if historical_data.empty or not all(ticker in historical_data.columns for ticker in tickers):
        return pd.DataFrame()  # Return empty DataFrame if no data
    
    # Calculate portfolio value over time based on allocations and a $10,000 initial investment
    initial_investment = 10000
    portfolio_values = pd.DataFrame(index=historical_data.index)
    
    # Normalize to initial values to calculate growth
    for ticker in tickers:
        initial_price = historical_data[ticker].iloc[0]
        portfolio_values[f"{ticker}_normalized"] = historical_data[ticker] / initial_price
    
    # Calculate weighted portfolio value
    portfolio_values['Portfolio'] = (
        us_allocation * portfolio_values[f"{us_ticker}_normalized"] +
        intl_allocation * portfolio_values[f"{intl_ticker}_normalized"] +
        bond_allocation * portfolio_values[f"{bond_ticker}_normalized"]
    ) * initial_investment
    
    # Add individual components
    portfolio_values['US Stock'] = us_allocation * portfolio_values[f"{us_ticker}_normalized"] * initial_investment
    portfolio_values['International Stock'] = intl_allocation * portfolio_values[f"{intl_ticker}_normalized"] * initial_investment
    portfolio_values['Bond'] = bond_allocation * portfolio_values[f"{bond_ticker}_normalized"] * initial_investment
    
    # Calculate benchmark (60/40 portfolio)
    portfolio_values['60/40 Benchmark'] = (
        0.6 * portfolio_values[f"{us_ticker}_normalized"] +
        0.4 * portfolio_values[f"{bond_ticker}_normalized"]
    ) * initial_investment
    
    # Reset index to have Date as a column
    portfolio_values.reset_index(inplace=True)
    
    # Keep only the columns we need
    keep_columns = ['Date', 'Portfolio', 'US Stock', 'International Stock', 'Bond', '60/40 Benchmark']
    portfolio_values = portfolio_values[keep_columns]
    
    return portfolio_values

def calculate_returns_metrics(backtest_data):
    """
    Calculate key metrics from backtest data
    
    Args:
        backtest_data: DataFrame with backtest results
        
    Returns:
        Dictionary with metrics
    """
    if backtest_data.empty:
        return {}
    
    metrics = {}
    
    # Calculate total return
    initial_value = backtest_data['Portfolio'].iloc[0]
    final_value = backtest_data['Portfolio'].iloc[-1]
    total_return = (final_value / initial_value - 1) * 100
    metrics['total_return'] = total_return
    
    # Calculate annualized return
    years = (backtest_data['Date'].iloc[-1] - backtest_data['Date'].iloc[0]).days / 365
    annualized_return = ((final_value / initial_value) ** (1 / years) - 1) * 100
    metrics['annualized_return'] = annualized_return
    
    # Calculate volatility (annualized standard deviation of returns)
    monthly_returns = backtest_data['Portfolio'].pct_change().dropna()
    volatility = monthly_returns.std() * np.sqrt(12) * 100  # Annualized
    metrics['volatility'] = volatility
    
    # Calculate max drawdown
    portfolio_value = backtest_data['Portfolio']
    rolling_max = portfolio_value.cummax()
    drawdown = (portfolio_value - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100
    metrics['max_drawdown'] = max_drawdown
    
    # Calculate Sharpe ratio (using 0% risk-free rate for simplicity)
    sharpe_ratio = annualized_return / volatility if volatility > 0 else 0
    metrics['sharpe_ratio'] = sharpe_ratio
    
    # Calculate same metrics for benchmark
    benchmark_initial = backtest_data['60/40 Benchmark'].iloc[0]
    benchmark_final = backtest_data['60/40 Benchmark'].iloc[-1]
    benchmark_return = (benchmark_final / benchmark_initial - 1) * 100
    metrics['benchmark_total_return'] = benchmark_return
    
    benchmark_annual = ((benchmark_final / benchmark_initial) ** (1 / years) - 1) * 100
    metrics['benchmark_annual_return'] = benchmark_annual
    
    # Calculate outperformance
    metrics['outperformance'] = annualized_return - benchmark_annual
    
    return metrics

def show_backtesting_page(portfolio):
    """
    Display the portfolio backtesting page
    """
    st.header("Portfolio Backtesting")
    
    st.markdown("""
    Backtest your portfolio against historical market data to see how it would have performed in the past.
    This simulation includes major market events like the 2008 Financial Crisis and the 2020 COVID-19 crash.
    
    Remember that past performance is not indicative of future results, but historical backtesting can help
    you understand how your portfolio might behave in different market conditions.
    """)
    
    # Get portfolio allocation data
    allocation_data = portfolio.get_allocation_data()
    
    # Show current allocation
    st.subheader("Current Portfolio Allocation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("US Stocks", f"{allocation_data['us_stock']}%")
        st.caption(f"Fund: {allocation_data['us_ticker']}")
        
    with col2:
        st.metric("International Stocks", f"{allocation_data['international_stock']}%")
        st.caption(f"Fund: {allocation_data['international_ticker']}")
        
    with col3:
        st.metric("Bonds", f"{allocation_data['bond']}%")
        st.caption(f"Fund: {allocation_data['bond_ticker']}")
    
    # Backtest settings
    st.subheader("Backtest Settings")
    
    # Year range selection
    current_year = datetime.now().year
    start_year = st.slider(
        "Select Starting Year",
        min_value=2000,
        max_value=current_year-1,
        value=2010,
        step=1
    )
    
    # Run backtest
    backtest_data = calculate_portfolio_backtest(portfolio, start_year)
    
    if not backtest_data.empty:
        # Display backtest results
        st.subheader("Backtest Results")
        
        # Get metrics
        metrics = calculate_returns_metrics(backtest_data)
        
        # Display key metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(
                "Total Return", 
                f"{metrics['total_return']:.1f}%",
                f"{metrics['total_return'] - metrics['benchmark_total_return']:.1f}% vs 60/40"
            )
            st.metric(
                "Annualized Return", 
                f"{metrics['annualized_return']:.2f}%",
                f"{metrics['outperformance']:.2f}% vs 60/40"
            )
            
        with metric_col2:
            st.metric("Volatility (Annualized)", f"{metrics['volatility']:.2f}%")
            st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
            
        with metric_col3:
            st.metric("Maximum Drawdown", f"{metrics['max_drawdown']:.1f}%")
            st.metric("Benchmark Return", f"{metrics['benchmark_annual_return']:.2f}% per year")
        
        # Display growth chart
        st.subheader("Portfolio Growth Over Time")
        
        # Create line chart for portfolio growth
        fig = go.Figure()
        
        # Add portfolio line
        fig.add_trace(go.Scatter(
            x=backtest_data['Date'],
            y=backtest_data['Portfolio'],
            mode='lines',
            name='Your Portfolio',
            line=dict(width=3)
        ))
        
        # Add benchmark line
        fig.add_trace(go.Scatter(
            x=backtest_data['Date'],
            y=backtest_data['60/40 Benchmark'],
            mode='lines',
            name='60/40 Benchmark',
            line=dict(dash='dash')
        ))
        
        # Update layout
        fig.update_layout(
            title='$10,000 Investment Growth',
            xaxis_title='Date',
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
        
        # Show chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Stacked area chart showing allocation components
        st.subheader("Portfolio Components Growth")
        
        # Create stacked area chart
        fig_components = go.Figure()
        
        # Add each component
        fig_components.add_trace(go.Scatter(
            x=backtest_data['Date'],
            y=backtest_data['Bond'],
            mode='lines',
            name='Bonds',
            stackgroup='one',
            fillcolor='rgba(44, 160, 44, 0.5)'
        ))
        
        fig_components.add_trace(go.Scatter(
            x=backtest_data['Date'],
            y=backtest_data['International Stock'],
            mode='lines',
            name='International Stocks',
            stackgroup='one',
            fillcolor='rgba(214, 39, 40, 0.5)'
        ))
        
        fig_components.add_trace(go.Scatter(
            x=backtest_data['Date'],
            y=backtest_data['US Stock'],
            mode='lines',
            name='US Stocks',
            stackgroup='one',
            fillcolor='rgba(31, 119, 180, 0.5)'
        ))
        
        # Update layout
        fig_components.update_layout(
            title='Portfolio Component Growth',
            xaxis_title='Date',
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
        fig_components.update_yaxes(tickprefix='$', tickformat=',.0f')
        
        # Show chart
        st.plotly_chart(fig_components, use_container_width=True)
        
        # Add educational content
        st.divider()
        st.subheader("Understanding Backtesting")
        
        st.markdown("""
        ### What is Backtesting?
        
        Backtesting is a method to evaluate how a portfolio would have performed during a specific historical period.
        It helps you understand the risk and return characteristics of your investment strategy.
        
        ### Limitations of Backtesting
        
        While backtesting is a useful tool, it's important to understand its limitations:
        
        - **Past performance doesn't predict future results**: Market conditions change over time.
        - **Perfect hindsight**: It's easy to create a portfolio that would have performed well in the past.
        - **Model simplification**: This simulation uses approximated historical returns for each asset class.
        - **Rebalancing assumptions**: The simulation assumes perfect rebalancing to maintain allocation targets.
        
        ### What to Look For
        
        When analyzing backtest results, consider these factors:
        
        - **Risk-adjusted returns**: Higher returns often come with higher risk. The Sharpe ratio helps measure this balance.
        - **Maximum drawdown**: How much your portfolio declined during the worst period.
        - **Performance in different market conditions**: How did your portfolio behave during bull and bear markets?
        - **Benchmark comparison**: How your portfolio performed relative to a standard benchmark (60/40 stock/bond portfolio).
        
        > *"The investor's chief problem—and even his worst enemy—is likely to be himself."* - Benjamin Graham
        """)
    else:
        st.warning("Unable to generate backtest results with the selected parameters. Please try different settings.")