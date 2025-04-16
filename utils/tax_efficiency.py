import pandas as pd
import numpy as np
from data.fund_data import get_fund_data

class TaxEfficiencyCalculator:
    def __init__(self):
        # Tax efficiency rankings (higher means more tax-inefficient)
        self.tax_efficiency_rankings = {
            "US Total Market": 3,
            "US Large Cap": 3,
            "US Small Cap": 4,
            "International Developed": 4,
            "International Emerging": 5,
            "US Total Bond": 5,
            "US Treasury": 6,
            "US TIPS": 6,
            "US Corporate": 7,
            "US High Yield": 7,
            "International Bond": 6,
            "REITs": 7
        }
        
        # Account tax benefits rankings (higher means more tax-advantaged)
        self.account_tax_rankings = {
            "401k": 5,
            "IRA": 5,
            "HSA": 6,
            "Taxable": 1
        }
        
    def get_fund_tax_efficiency(self, fund_ticker):
        """Get the tax efficiency ranking for a specific fund"""
        fund_data = get_fund_data()
        fund_info = fund_data[fund_data['Ticker'] == fund_ticker]
        
        if not fund_info.empty:
            fund_category = fund_info['Category'].values[0]
            return self.tax_efficiency_rankings.get(fund_category, 3)
        
        return 3  # Default ranking if fund not found
    
    def generate_recommendations(self, portfolio):
        """Generate tax-efficient fund placement recommendations"""
        # Get tax efficiency values for the selected funds
        us_tax_efficiency = self.get_fund_tax_efficiency(portfolio.us_stock_fund)
        intl_tax_efficiency = self.get_fund_tax_efficiency(portfolio.international_stock_fund)
        bond_tax_efficiency = self.get_fund_tax_efficiency(portfolio.bond_fund)
        
        # Create a DataFrame of fund information
        funds_df = pd.DataFrame({
            'Fund': [portfolio.us_stock_fund, portfolio.international_stock_fund, portfolio.bond_fund],
            'Type': ['US Stocks', 'International Stocks', 'Bonds'],
            'Allocation': [
                portfolio.us_stock_allocation, 
                portfolio.international_stock_allocation, 
                portfolio.bond_allocation
            ],
            'Tax Inefficiency': [us_tax_efficiency, intl_tax_efficiency, bond_tax_efficiency]
        })
        
        # Sort funds by tax inefficiency (most tax-inefficient first)
        funds_df = funds_df.sort_values('Tax Inefficiency', ascending=False)
        
        # Create a DataFrame of accounts with their values and tax advantages
        accounts_df = pd.DataFrame({
            'Account': list(portfolio.account_values.keys()),
            'Value': list(portfolio.account_values.values()),
            'Tax Advantage': [self.account_tax_rankings.get(acct, 1) for acct in portfolio.account_values.keys()]
        })
        
        # Sort accounts by tax advantage (highest tax advantage first)
        accounts_df = accounts_df.sort_values('Tax Advantage', ascending=False)
        
        # Calculate dollar amounts needed for each fund
        total_portfolio = sum(portfolio.account_values.values())
        funds_df['Dollar Amount'] = funds_df['Allocation'] * total_portfolio / 100
        
        # Create recommendations
        recommendations = []
        
        # Copy DataFrames to avoid modifying originals
        remaining_funds = funds_df.copy()
        remaining_accounts = accounts_df.copy()
        
        # Allocate funds to accounts based on tax-efficiency
        while not remaining_funds.empty and not remaining_accounts.empty:
            # Get the most tax-inefficient fund and most tax-advantaged account
            current_fund = remaining_funds.iloc[0]
            current_account = remaining_accounts.iloc[0]
            
            # Determine how much of the fund to place in this account
            amount_to_place = min(current_fund['Dollar Amount'], current_account['Value'])
            
            # Record the recommendation
            if amount_to_place > 0:
                recommendations.append({
                    'Fund': current_fund['Fund'],
                    'Fund Type': current_fund['Type'],
                    'Account': current_account['Account'],
                    'Amount': amount_to_place,
                    'Percent of Portfolio': round(amount_to_place / total_portfolio * 100, 2)
                })
            
            # Update remaining amounts
            remaining_fund_amount = current_fund['Dollar Amount'] - amount_to_place
            remaining_account_value = current_account['Value'] - amount_to_place
            
            # Remove fund or account if fully allocated
            if remaining_fund_amount <= 0:
                remaining_funds = remaining_funds.iloc[1:].copy()
            else:
                remaining_funds.iloc[0, remaining_funds.columns.get_loc('Dollar Amount')] = remaining_fund_amount
                
            if remaining_account_value <= 0:
                remaining_accounts = remaining_accounts.iloc[1:].copy()
            else:
                remaining_accounts.iloc[0, remaining_accounts.columns.get_loc('Value')] = remaining_account_value
        
        return pd.DataFrame(recommendations)
    
    def get_tax_efficiency_explanation(self):
        """Return explanation of tax efficiency principles"""
        return {
            "title": "Tax-Efficiency Principles",
            "explanations": [
                {
                    "principle": "1. Bonds in Tax-Advantaged Accounts",
                    "description": "Bond funds generate income that is taxed at ordinary income rates. Place bond funds in tax-advantaged accounts like 401(k)s or IRAs to shield this income from taxes."
                },
                {
                    "principle": "2. International Stocks in Taxable Accounts",
                    "description": "International funds may benefit from foreign tax credits, which are only available in taxable accounts. However, consider placing high-yielding international funds in tax-advantaged accounts."
                },
                {
                    "principle": "3. Total US Stock Market Funds in Taxable Accounts",
                    "description": "Total market index funds are relatively tax-efficient due to low turnover and qualified dividend treatment. These can be good candidates for taxable accounts."
                },
                {
                    "principle": "4. HSA Optimization",
                    "description": "Health Savings Accounts (HSAs) offer triple tax advantages (tax-deductible contributions, tax-free growth, and tax-free withdrawals for medical expenses). Prioritize these for your most tax-inefficient funds."
                },
                {
                    "principle": "5. Asset Location Hierarchy",
                    "description": "From most to least tax-efficient: HSA > Roth IRA > Traditional IRA/401(k) > Taxable accounts. Allocate funds according to their tax efficiency and this hierarchy."
                }
            ]
        }
