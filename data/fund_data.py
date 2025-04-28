import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_fund_data():
    """
    Return a DataFrame of fund data including tickers, expense ratios, and categories
    """
    # Data for popular Boglehead funds
    data = {
        "Provider": [
            # Vanguard
            "Vanguard", "Vanguard", "Vanguard", "Vanguard", "Vanguard", "Vanguard", 
            "Vanguard", "Vanguard", "Vanguard", "Vanguard", "Vanguard", "Vanguard",
            
            # Fidelity
            "Fidelity", "Fidelity", "Fidelity", "Fidelity", "Fidelity", "Fidelity",
            "Fidelity", "Fidelity", "Fidelity", 
            
            # iShares
            "iShares", "iShares", "iShares", "iShares", "iShares", "iShares",
            
            # Schwab
            "Schwab", "Schwab", "Schwab", "Schwab", "Schwab", "Schwab"
        ],
        
        "Fund Name": [
            # Vanguard
            "Vanguard Total Stock Market ETF", 
            "Vanguard Total Stock Market Index Fund Admiral", 
            "Vanguard S&P 500 ETF",
            "Vanguard Total International Stock ETF",
            "Vanguard Total International Stock Index Fund Admiral",
            "Vanguard FTSE Developed Markets ETF",
            "Vanguard FTSE Emerging Markets ETF",
            "Vanguard Total Bond Market ETF",
            "Vanguard Total Bond Market Index Fund Admiral",
            "Vanguard Intermediate-Term Treasury ETF",
            "Vanguard REIT ETF",
            "Vanguard Total World Stock ETF",
            
            # Fidelity
            "Fidelity ZERO Total Market Index Fund",
            "Fidelity Total Market Index Fund",
            "Fidelity ZERO International Index Fund",
            "Fidelity Total International Index Fund",
            "Fidelity U.S. Bond Index Fund",
            "Fidelity ZERO Large Cap Index Fund",
            "Fidelity 500 Index Fund",
            "Fidelity Emerging Markets Index Fund",
            "Fidelity Real Estate Index Fund",
            
            # iShares
            "iShares Core S&P Total U.S. Stock Market ETF",
            "iShares Core S&P 500 ETF",
            "iShares Core MSCI Total International Stock ETF",
            "iShares Core MSCI EAFE ETF",
            "iShares Core MSCI Emerging Markets ETF",
            "iShares Core U.S. Aggregate Bond ETF",
            
            # Schwab
            "Schwab Total Stock Market Index Fund",
            "Schwab S&P 500 Index Fund",
            "Schwab International Index Fund",
            "Schwab Emerging Markets Equity ETF",
            "Schwab U.S. Aggregate Bond Index Fund",
            "Schwab U.S. REIT ETF"
        ],
        
        "Ticker": [
            # Vanguard
            "VTI", "VTSAX", "VOO", "VXUS", "VTIAX", "VEA", 
            "VWO", "BND", "VBTLX", "VGIT", "VNQ", "VT",
            
            # Fidelity
            "FZROX", "FSKAX", "FZILX", "FTIHX", "FXNAX", 
            "FNILX", "FXAIX", "FPADX", "FSRNX",
            
            # iShares
            "ITOT", "IVV", "IXUS", "IEFA", "IEMG", "AGG",
            
            # Schwab
            "SWTSX", "SWPPX", "SWISX", "SCHE", "SWAGX", "SCHH"
        ],
        
        "Category": [
            # Vanguard
            "US Total Market", "US Total Market", "US Large Cap", 
            "International Developed", "International Developed", "International Developed", 
            "International Emerging", "US Total Bond", "US Total Bond", 
            "US Treasury", "REITs", "US Total Market",
            
            # Fidelity
            "US Total Market", "US Total Market", "International Developed", 
            "International Developed", "US Total Bond", "US Large Cap", 
            "US Large Cap", "International Emerging", "REITs",
            
            # iShares
            "US Total Market", "US Large Cap", "International Developed", 
            "International Developed", "International Emerging", "US Total Bond",
            
            # Schwab
            "US Total Market", "US Large Cap", "International Developed", 
            "International Emerging", "US Total Bond", "REITs"
        ],
        
        "Expense Ratio": [
            # Vanguard
            0.0003, 0.0004, 0.0003, 0.0008, 0.0011, 0.0005, 
            0.0008, 0.0003, 0.0005, 0.0005, 0.0012, 0.0007,
            
            # Fidelity
            0.0000, 0.0015, 0.0000, 0.0006, 0.0025, 
            0.0000, 0.0015, 0.0012, 0.0019,
            
            # iShares
            0.0003, 0.0003, 0.0009, 0.0007, 0.0009, 0.0004,
            
            # Schwab
            0.0003, 0.0002, 0.0006, 0.0011, 0.0004, 0.0007
        ],
        
        "Asset Class": [
            # Vanguard
            "Stocks", "Stocks", "Stocks", "Stocks", "Stocks", "Stocks", 
            "Stocks", "Bonds", "Bonds", "Bonds", "Stocks", "Stocks",
            
            # Fidelity
            "Stocks", "Stocks", "Stocks", "Stocks", "Bonds", 
            "Stocks", "Stocks", "Stocks", "Stocks",
            
            # iShares
            "Stocks", "Stocks", "Stocks", "Stocks", "Stocks", "Bonds",
            
            # Schwab
            "Stocks", "Stocks", "Stocks", "Stocks", "Bonds", "Stocks"
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df

def get_fund_alternatives(fund_type):
    """
    Get alternative funds for a specific fund type
    
    Parameters:
    - fund_type: 'US Total Market', 'International Developed', etc.
    
    Returns:
    - DataFrame of funds matching the type
    """
    df = get_fund_data()
    return df[df['Category'] == fund_type].sort_values('Expense Ratio')

def get_historical_prices(tickers, years=5):
    """
    Generate realistic historical price data for the specified tickers
    
    Parameters:
    - tickers: List of fund tickers to generate data for
    - years: Number of years of historical data to generate
    
    Returns:
    - DataFrame with historical price data
    """
    # Get fund information
    fund_data = get_fund_data()
    
    # Generate dates (monthly data points)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)
    dates = pd.date_range(start=start_date, end=end_date, freq='ME')  # Month End frequency
    
    # Create a DataFrame to store results
    price_data = pd.DataFrame({'Date': dates})
    
    # Base market data - we'll simulate market movements first
    # This ensures that funds in similar categories move together
    # and respond to the same market events
    
    # Generate base market movements (S&P 500 proxy)
    np.random.seed(42)  # For reproducibility
    market_monthly_return = 0.007  # ~8.7% annual return
    market_monthly_vol = 0.04      # ~14% annual volatility
    
    # Generate random market returns
    n_months = len(dates)
    market_random_returns = np.random.normal(market_monthly_return, market_monthly_vol, n_months)
    
    # Add in a few market shocks (crashes and recoveries)
    # Simulate 2 significant events over the period
    if n_months > 24:
        # First event (negative)
        shock_idx1 = n_months // 3
        market_random_returns[shock_idx1] = -0.15
        market_random_returns[shock_idx1+1] = -0.08
        market_random_returns[shock_idx1+2:shock_idx1+5] = 0.03
        
        # Second event (positive)
        shock_idx2 = 2 * n_months // 3
        market_random_returns[shock_idx2:shock_idx2+3] = 0.04
    
    # Calculate cumulative market returns
    market_cumulative = (1 + market_random_returns).cumprod()
    
    # Define accurate base performance characteristics for different categories
    # with realistic correlations to the overall market
    category_params = {
        'US Total Market': {
            'correlation': 0.98,  # Very high correlation with market
            'beta': 1.0,         # Same as market
            'alpha': 0.0002,     # Small positive alpha
            'tracking_error': 0.002,  # Very low tracking error
            'start_price': 250   # Reasonable starting price
        },
        'US Large Cap': {
            'correlation': 0.99,  # Almost perfect correlation with market
            'beta': 0.98,        # Slightly less volatile than market
            'alpha': 0.0001,     # Tiny positive alpha
            'tracking_error': 0.001,  # Very low tracking error
            'start_price': 480   # Higher price point
        },
        'International Developed': {
            'correlation': 0.85,  # High but not perfect correlation
            'beta': 1.05,        # Slightly more volatile
            'alpha': -0.0005,    # Slight negative alpha
            'tracking_error': 0.008,  # Higher tracking error
            'start_price': 75    # Lower typical price
        },
        'International Emerging': {
            'correlation': 0.7,   # Moderate correlation
            'beta': 1.2,         # Higher volatility
            'alpha': 0.0008,     # Potential for higher returns
            'tracking_error': 0.015,  # Higher tracking error
            'start_price': 55    # Lower typical price
        },
        'US Total Bond': {
            'correlation': -0.2,  # Negative correlation with stocks
            'beta': 0.2,         # Much lower volatility
            'alpha': 0.0001,     # Small positive alpha
            'tracking_error': 0.002,  # Very low tracking error
            'start_price': 110   # Bond fund prices are typically more stable
        },
        'US Treasury': {
            'correlation': -0.3,  # Stronger negative correlation
            'beta': 0.15,        # Very low volatility
            'alpha': 0.0,        # No alpha
            'tracking_error': 0.001,  # Very low tracking error
            'start_price': 115   # Government bond funds are stable
        },
        'REITs': {
            'correlation': 0.6,   # Moderate correlation
            'beta': 1.1,         # Higher volatility
            'alpha': 0.0007,     # Potential for higher returns
            'tracking_error': 0.01,   # Higher tracking error
            'start_price': 120   # REIT prices
        }
    }
    
    # Dictionary to store generated category data
    category_data = {}
    
    # Generate category-level price data first
    for category, params in category_params.items():
        # Generate correlated returns with the market
        category_specific = np.random.normal(0, params['tracking_error'], n_months)
        
        # Calculate returns based on market returns, beta, alpha and specific returns
        category_returns = params['alpha'] + params['beta'] * market_random_returns + category_specific
        
        # Calculate cumulative returns
        category_cumulative = (1 + category_returns).cumprod()
        
        # Calculate prices
        category_prices = params['start_price'] * category_cumulative
        
        # Store category data
        category_data[category] = category_prices
    
    # Generate price series for each ticker
    for ticker in tickers:
        if ticker in fund_data['Ticker'].values:
            # Get the fund's category
            fund_info = fund_data[fund_data['Ticker'] == ticker].iloc[0]
            category = fund_info['Category']
            
            # Get expense ratio (this will affect long-term performance)
            expense_ratio = fund_info['Expense Ratio']
            
            # Use the category data as a base
            if category in category_data:
                base_prices = category_data[category]
                
                # Add fund-specific variation 
                # This represents tracking error, securities lending income differences, etc.
                # Use hash of ticker for deterministic but unique behavior
                np.random.seed(hash(ticker) % 10000)
                
                # Very small fund-specific variations (these are index funds after all)
                # Funds with lower expense ratios will slightly outperform over time
                tracking_diff = 0.0005 - expense_ratio  # Better performance for lower expense ratios
                
                # Generate small random tracking differences
                fund_tracking_error = np.random.normal(tracking_diff/n_months, 0.001, n_months)
                
                # Calculate fund-specific returns
                fund_returns = (base_prices[1:] / base_prices[:-1] - 1) + fund_tracking_error[1:]
                fund_returns = np.insert(fund_returns, 0, 0)  # First month has no return
                
                # Calculate cumulative returns
                fund_cumulative = (1 + fund_returns).cumprod()
                
                # Calculate prices - start near the category price but with slight variations
                start_variation = 1.0 + (hash(ticker) % 20 - 10) / 1000  # ±1% variation
                fund_start_price = base_prices[0] * start_variation
                fund_prices = fund_start_price * fund_cumulative
                
                # Add to DataFrame
                price_data[ticker] = fund_prices
    
    return price_data
