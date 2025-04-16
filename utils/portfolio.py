import pandas as pd
import numpy as np
from data.fund_data import get_fund_data
import utils.db as db

class Portfolio:
    def __init__(self, portfolio_id=None, name="My Portfolio"):
        # Portfolio ID and name
        self.id = portfolio_id
        self.name = name
        
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
        
        # If portfolio_id is provided, load from the database
        if portfolio_id:
            self.load_from_db(portfolio_id)
        
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
        
        # Set portfolio ID and name if provided
        portfolio.id = data.get("id")
        portfolio.name = data.get("name", "My Portfolio")
        
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
        
    def save_to_db(self, user_id=1):
        """
        Save the portfolio to the database
        
        Args:
            user_id: The user ID to associate with this portfolio
            
        Returns:
            int: The portfolio ID in the database
        """
        try:
            # Convert portfolio to database format
            portfolio_data = {
                'name': self.name,
                'initial_investment': self.initial_investment,
                'monthly_contribution': self.monthly_contribution,
                'years_to_grow': self.years_to_grow,
                'us_stock': self.us_stock_allocation,
                'international_stock': self.international_stock_allocation,
                'bond': self.bond_allocation,
                'funds': {
                    'US Stock': {
                        'ticker': self.us_stock_fund,
                        'name': self.get_fund_name(self.us_stock_fund),
                        'expense_ratio': self.get_fund_expense_ratio(self.us_stock_fund)
                    },
                    'International Stock': {
                        'ticker': self.international_stock_fund,
                        'name': self.get_fund_name(self.international_stock_fund),
                        'expense_ratio': self.get_fund_expense_ratio(self.international_stock_fund)
                    },
                    'Bond': {
                        'ticker': self.bond_fund,
                        'name': self.get_fund_name(self.bond_fund),
                        'expense_ratio': self.get_fund_expense_ratio(self.bond_fund)
                    }
                }
            }
            
            # Save to the database
            db_portfolio = db.save_portfolio(portfolio_data, user_id)
            
            # Update our ID
            if db_portfolio:
                self.id = db_portfolio.id
                return self.id
        except Exception as e:
            print(f"Error saving portfolio to database: {e}")
            return None
            
    def load_from_db(self, portfolio_id, user_id=1):
        """
        Load a portfolio from the database
        
        Args:
            portfolio_id: The portfolio ID to load
            user_id: The user ID associated with the portfolio
            
        Returns:
            bool: Success or failure
        """
        try:
            # Load from database
            portfolio_data = db.load_portfolio(portfolio_id, user_id)
            
            if portfolio_data:
                # Update portfolio with loaded data
                self.name = portfolio_data.get('name', 'My Portfolio')
                self.initial_investment = portfolio_data.get('initial_investment', 10000)
                self.monthly_contribution = portfolio_data.get('monthly_contribution', 500)
                self.years_to_grow = portfolio_data.get('years_to_grow', 30)
                
                # Update allocations
                self.us_stock_allocation = portfolio_data.get('us_stock', 60)
                self.international_stock_allocation = portfolio_data.get('international_stock', 30)
                self.bond_allocation = portfolio_data.get('bond', 10)
                
                # Load fund selections
                funds = portfolio_data.get('funds', {})
                
                if 'US Stock' in funds:
                    self.us_stock_fund = funds['US Stock'].get('ticker', 'VTI')
                    
                if 'International Stock' in funds:
                    self.international_stock_fund = funds['International Stock'].get('ticker', 'VXUS')
                    
                if 'Bond' in funds:
                    self.bond_fund = funds['Bond'].get('ticker', 'BND')
                
                return True
            return False
            
        except Exception as e:
            print(f"Error loading portfolio from database: {e}")
            return False
            
    def get_fund_name(self, ticker):
        """Get the name of a fund by ticker"""
        fund_data = self.fund_data
        name = fund_data[fund_data['Ticker'] == ticker]['Fund Name'].values
        return name[0] if len(name) > 0 else ""
        
    def get_fund_expense_ratio(self, ticker):
        """Get the expense ratio of a fund by ticker"""
        fund_data = self.fund_data
        expense = fund_data[fund_data['Ticker'] == ticker]['Expense Ratio'].values
        return float(expense[0]) if len(expense) > 0 else 0.0
        
    @classmethod
    def get_user_portfolios(cls, user_id=1):
        """
        Get a list of all portfolios for a user
        
        Args:
            user_id: The user ID to find portfolios for
            
        Returns:
            list: List of portfolio overview dicts with id and name
        """
        try:
            return db.get_user_portfolios(user_id)
        except Exception as e:
            print(f"Error getting user portfolios: {e}")
            return []
            
    @classmethod
    def delete_portfolio(cls, portfolio_id, user_id=1):
        """
        Delete a portfolio
        
        Args:
            portfolio_id: The portfolio ID to delete
            user_id: The user ID associated with the portfolio
            
        Returns:
            bool: Success or failure
        """
        try:
            return db.delete_portfolio(portfolio_id, user_id)
        except Exception as e:
            print(f"Error deleting portfolio: {e}")
            return False
