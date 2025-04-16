import pandas as pd

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
