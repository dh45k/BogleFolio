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
    Generate historical price data for the specified tickers
    
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
    dates = pd.date_range(start=start_date, end=end_date, freq='ME')  # Month end frequency
    
    # Create a DataFrame to store results
    price_data = pd.DataFrame({'Date': dates})
    
    # Define base performance characteristics for different categories
    category_returns = {
        'US Total Market': {'annual_return': 0.10, 'volatility': 0.16},
        'US Large Cap': {'annual_return': 0.09, 'volatility': 0.15},
        'International Developed': {'annual_return': 0.07, 'volatility': 0.18},
        'International Emerging': {'annual_return': 0.08, 'volatility': 0.22},
        'US Total Bond': {'annual_return': 0.04, 'volatility': 0.05},
        'US Treasury': {'annual_return': 0.035, 'volatility': 0.04},
        'REITs': {'annual_return': 0.08, 'volatility': 0.19}
    }
    
    # Generate price series for each ticker
    for ticker in tickers:
        if ticker in fund_data['Ticker'].values:
            # Get the fund's category
            fund_info = fund_data[fund_data['Ticker'] == ticker].iloc[0]
            category = fund_info['Category']
            
            # Get category parameters
            params = category_returns.get(category, {'annual_return': 0.08, 'volatility': 0.15})
            annual_return = params['annual_return']
            volatility = params['volatility']
            
            # Generate monthly returns with some randomness but following the category pattern
            monthly_return = annual_return / 12
            monthly_volatility = volatility / np.sqrt(12)
            
            # Create a slight variation for each fund in the same category
            fund_specific_factor = 1.0 + (hash(ticker) % 10 - 5) / 100
            
            # Generate random returns
            np.random.seed(hash(ticker) % 10000)  # Use ticker as seed for reproducibility
            random_returns = np.random.normal(
                monthly_return * fund_specific_factor, 
                monthly_volatility, 
                len(dates)
            )
            
            # Calculate cumulative returns
            cumulative_returns = (1 + random_returns).cumprod()
            
            # Start price between $50 and $200 based on ticker
            start_price = 100 + (hash(ticker) % 150)
            prices = start_price * cumulative_returns
            
            # Add to DataFrame
            price_data[ticker] = prices
    
    return price_data
