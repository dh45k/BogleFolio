import pandas as pd
import numpy as np
from data.fund_data import get_fund_data

class Portfolio:
    def __init__(self):
        # Default allocation percentages
        self.us_stock_allocation = 60
        self.international_stock_allocation = 30
        self.bond_allocation = 10
        
        # Default funds
        self.us_stock_fund = "VTI"
        self.international_stock_fund = "VXUS"
        self.bond_fund = "BND"
        
        # Default account values
        self.account_values = {
            "401k": 100000,
            "IRA": 50000,
            "HSA": 20000,
            "Taxable": 30000
        }
        
        # Initial investment amount
        self.initial_investment = sum(self.account_values.values())
        
        # Contribution settings
        self.monthly_contribution = 1000
        self.years_to_grow = 30
        self.expected_return_us = 7.0
        self.expected_return_intl = 6.5
        self.expected_return_bond = 3.0
        
        # Fund data
        self.fund_data = get_fund_data()
        
    def get_total_allocation(self):
        return self.us_stock_allocation + self.international_stock_allocation + self.bond_allocation
    
    def update_allocation(self, us_stock, international_stock, bond):
        """Update the portfolio allocation percentages"""
        self.us_stock_allocation = us_stock
        self.international_stock_allocation = international_stock
        self.bond_allocation = bond
        
    def update_funds(self, us_stock_fund, international_stock_fund, bond_fund):
        """Update the funds in the portfolio"""
        self.us_stock_fund = us_stock_fund
        self.international_stock_fund = international_stock_fund
        self.bond_fund = bond_fund
        
    def update_account_values(self, account_values):
        """Update the account values"""
        self.account_values = account_values
        self.initial_investment = sum(self.account_values.values())
        
    def get_allocation_data(self):
        """Return allocation data in a format suitable for plotting"""
        return {
            "Category": ["US Stocks", "International Stocks", "Bonds"],
            "Allocation": [
                self.us_stock_allocation, 
                self.international_stock_allocation, 
                self.bond_allocation
            ],
            "Fund": [
                self.us_stock_fund,
                self.international_stock_fund,
                self.bond_fund
            ]
        }
        
    def get_weighted_expense_ratio(self):
        """Calculate weighted expense ratio for the portfolio"""
        fund_data = self.fund_data
        
        us_expense = fund_data[fund_data['Ticker'] == self.us_stock_fund]['Expense Ratio'].values[0]
        intl_expense = fund_data[fund_data['Ticker'] == self.international_stock_fund]['Expense Ratio'].values[0]
        bond_expense = fund_data[fund_data['Ticker'] == self.bond_fund]['Expense Ratio'].values[0]
        
        weighted_ratio = (
            (self.us_stock_allocation / 100) * us_expense +
            (self.international_stock_allocation / 100) * intl_expense +
            (self.bond_allocation / 100) * bond_expense
        )
        
        return weighted_ratio
    
    def get_weighted_return(self):
        """Calculate weighted expected return for the portfolio"""
        weighted_return = (
            (self.us_stock_allocation / 100) * self.expected_return_us +
            (self.international_stock_allocation / 100) * self.expected_return_intl +
            (self.bond_allocation / 100) * self.expected_return_bond
        )
        
        return weighted_return
    
    def to_dict(self):
        """Convert portfolio to dictionary for saving"""
        return {
            "us_stock_allocation": self.us_stock_allocation,
            "international_stock_allocation": self.international_stock_allocation,
            "bond_allocation": self.bond_allocation,
            "us_stock_fund": self.us_stock_fund,
            "international_stock_fund": self.international_stock_fund,
            "bond_fund": self.bond_fund,
            "account_values": self.account_values,
            "initial_investment": self.initial_investment,
            "monthly_contribution": self.monthly_contribution,
            "years_to_grow": self.years_to_grow,
            "expected_return_us": self.expected_return_us,
            "expected_return_intl": self.expected_return_intl,
            "expected_return_bond": self.expected_return_bond
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create portfolio from dictionary"""
        portfolio = cls()
        
        portfolio.us_stock_allocation = data.get("us_stock_allocation", 60)
        portfolio.international_stock_allocation = data.get("international_stock_allocation", 30)
        portfolio.bond_allocation = data.get("bond_allocation", 10)
        
        portfolio.us_stock_fund = data.get("us_stock_fund", "VTI")
        portfolio.international_stock_fund = data.get("international_stock_fund", "VXUS")
        portfolio.bond_fund = data.get("bond_fund", "BND")
        
        portfolio.account_values = data.get("account_values", {
            "401k": 100000,
            "IRA": 50000,
            "HSA": 20000,
            "Taxable": 30000
        })
        
        portfolio.initial_investment = data.get("initial_investment", sum(portfolio.account_values.values()))
        portfolio.monthly_contribution = data.get("monthly_contribution", 1000)
        portfolio.years_to_grow = data.get("years_to_grow", 30)
        portfolio.expected_return_us = data.get("expected_return_us", 7.0)
        portfolio.expected_return_intl = data.get("expected_return_intl", 6.5)
        portfolio.expected_return_bond = data.get("expected_return_bond", 3.0)
        
        return portfolio
