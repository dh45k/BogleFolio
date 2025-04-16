import pandas as pd
import numpy as np

def calculate_compound_growth(initial_investment, monthly_contribution, years, annual_return_percent):
    """
    Calculate compound growth over time
    
    Parameters:
    - initial_investment: Initial amount invested
    - monthly_contribution: Monthly contribution amount
    - years: Number of years to project
    - annual_return_percent: Expected annual return percentage
    
    Returns:
    - DataFrame with growth projections by month
    """
    # Convert annual return to monthly rate
    monthly_rate = (1 + annual_return_percent/100) ** (1/12) - 1
    
    # Create array of months
    months = np.arange(years * 12 + 1)
    
    # Initialize arrays for values
    balance = np.zeros(len(months))
    contributions = np.zeros(len(months))
    earnings = np.zeros(len(months))
    
    # Set initial values
    balance[0] = initial_investment
    contributions[0] = initial_investment
    
    # Calculate growth for each month
    for i in range(1, len(months)):
        # Previous balance plus new contribution
        prev_balance_with_contribution = balance[i-1] + monthly_contribution
        
        # New balance with growth
        balance[i] = prev_balance_with_contribution * (1 + monthly_rate)
        
        # Track total contributions
        contributions[i] = contributions[i-1] + monthly_contribution
        
        # Calculate earnings (balance minus contributions)
        earnings[i] = balance[i] - contributions[i]
    
    # Create DataFrame with results
    df = pd.DataFrame({
        'Month': months,
        'Year': months // 12,
        'Balance': balance,
        'Contributions': contributions,
        'Earnings': earnings
    })
    
    return df

def calculate_portfolio_growth(portfolio):
    """
    Calculate growth for each component of the portfolio and combined total
    
    Parameters:
    - portfolio: Portfolio object containing allocation and return expectations
    
    Returns:
    - DataFrame with growth projections
    """
    # Calculate weighted monthly contribution based on allocation
    us_contribution = portfolio.monthly_contribution * (portfolio.us_stock_allocation / 100)
    intl_contribution = portfolio.monthly_contribution * (portfolio.international_stock_allocation / 100)
    bond_contribution = portfolio.monthly_contribution * (portfolio.bond_allocation / 100)
    
    # Calculate initial investment for each component
    total_investment = portfolio.initial_investment
    us_initial = total_investment * (portfolio.us_stock_allocation / 100)
    intl_initial = total_investment * (portfolio.international_stock_allocation / 100)
    bond_initial = total_investment * (portfolio.bond_allocation / 100)
    
    # Calculate growth for each component
    us_growth = calculate_compound_growth(
        us_initial, 
        us_contribution, 
        portfolio.years_to_grow, 
        portfolio.expected_return_us
    )
    
    intl_growth = calculate_compound_growth(
        intl_initial, 
        intl_contribution, 
        portfolio.years_to_grow, 
        portfolio.expected_return_intl
    )
    
    bond_growth = calculate_compound_growth(
        bond_initial, 
        bond_contribution, 
        portfolio.years_to_grow, 
        portfolio.expected_return_bond
    )
    
    # Calculate total portfolio growth (annual data points only)
    years = np.arange(portfolio.years_to_grow + 1)
    
    # Create a new DataFrame with just the years we want
    annual_data = []
    
    for year in years:
        # Get the data for this year from each component
        us_year_data = us_growth[us_growth['Year'] == year].iloc[0] if not us_growth[us_growth['Year'] == year].empty else None
        intl_year_data = intl_growth[intl_growth['Year'] == year].iloc[0] if not intl_growth[intl_growth['Year'] == year].empty else None
        bond_year_data = bond_growth[bond_growth['Year'] == year].iloc[0] if not bond_growth[bond_growth['Year'] == year].empty else None
        
        # Make sure we have data for all components
        if us_year_data is not None and intl_year_data is not None and bond_year_data is not None:
            us_balance = us_year_data['Balance']
            intl_balance = intl_year_data['Balance']
            bond_balance = bond_year_data['Balance']
            
            us_contribution = us_year_data['Contributions']
            intl_contribution = intl_year_data['Contributions']
            bond_contribution = bond_year_data['Contributions']
            
            annual_data.append({
                'Year': year,
                'US Stocks': us_balance,
                'International Stocks': intl_balance,
                'Bonds': bond_balance,
                'Total Balance': us_balance + intl_balance + bond_balance,
                'Total Contributions': us_contribution + intl_contribution + bond_contribution
            })
    
    # Create the DataFrame
    total_growth = pd.DataFrame(annual_data)
    
    # Calculate total earnings
    total_growth['Total Earnings'] = total_growth['Total Balance'] - total_growth['Total Contributions']
    
    return total_growth

def calculate_fee_impact(portfolio, alternative_expense_ratio=None):
    """
    Calculate the impact of expense ratios on long-term growth
    
    Parameters:
    - portfolio: Portfolio object
    - alternative_expense_ratio: Alternative expense ratio to compare against
    
    Returns:
    - DataFrame with comparison
    """
    # Get current weighted expense ratio
    current_expense_ratio = portfolio.get_weighted_expense_ratio()
    
    # If no alternative provided, use half the current for comparison
    if alternative_expense_ratio is None:
        alternative_expense_ratio = current_expense_ratio / 2
    
    # Calculate expected return with fees
    expected_return = portfolio.get_weighted_return()
    net_return_current = expected_return - current_expense_ratio
    net_return_alternative = expected_return - alternative_expense_ratio
    
    # Calculate growth with current expense ratio
    growth_current = calculate_compound_growth(
        portfolio.initial_investment,
        portfolio.monthly_contribution,
        portfolio.years_to_grow,
        net_return_current * 100  # Convert to percentage
    )
    
    # Calculate growth with alternative expense ratio
    growth_alternative = calculate_compound_growth(
        portfolio.initial_investment,
        portfolio.monthly_contribution,
        portfolio.years_to_grow,
        net_return_alternative * 100  # Convert to percentage
    )
    
    # Get annual data points only
    years = np.arange(portfolio.years_to_grow + 1)
    
    # Create a new DataFrame with just the years we want
    comparison_data = []
    
    for year in years:
        # Get the data for this year from each growth calculation
        current_year_data = growth_current[growth_current['Year'] == year].iloc[0] if not growth_current[growth_current['Year'] == year].empty else None
        alt_year_data = growth_alternative[growth_alternative['Year'] == year].iloc[0] if not growth_alternative[growth_alternative['Year'] == year].empty else None
        
        # Make sure we have data for both
        if current_year_data is not None and alt_year_data is not None:
            current_balance = current_year_data['Balance']
            alt_balance = alt_year_data['Balance']
            
            comparison_data.append({
                'Year': year,
                f'Balance (Expense Ratio: {current_expense_ratio:.3%})': current_balance,
                f'Balance (Expense Ratio: {alternative_expense_ratio:.3%})': alt_balance,
                'Fee Impact': alt_balance - current_balance
            })
    
    # Create comparison DataFrame
    comparison = pd.DataFrame(comparison_data)
    
    return comparison
