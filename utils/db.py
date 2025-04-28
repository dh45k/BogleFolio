import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# Create a base class for our ORM models
Base = declarative_base()

# Define our database models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship with the portfolios table
    portfolios = relationship('Portfolio', back_populates='user')
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Portfolio(Base):
    __tablename__ = 'portfolios'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    initial_investment = Column(Float, default=10000)
    monthly_contribution = Column(Float, default=500)
    years_to_grow = Column(Integer, default=30)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='portfolios')
    allocations = relationship('Allocation', back_populates='portfolio')
    fund_selections = relationship('FundSelection', back_populates='portfolio')
    
    def __repr__(self):
        return f"<Portfolio(name='{self.name}', user_id={self.user_id})>"


class Allocation(Base):
    __tablename__ = 'allocations'
    
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    us_stock = Column(Float, default=60.0)
    international_stock = Column(Float, default=30.0)
    bond = Column(Float, default=10.0)
    
    # Relationship
    portfolio = relationship('Portfolio', back_populates='allocations')
    
    def __repr__(self):
        return f"<Allocation(portfolio_id={self.portfolio_id}, us_stock={self.us_stock}, international_stock={self.international_stock}, bond={self.bond})>"


class FundSelection(Base):
    __tablename__ = 'fund_selections'
    
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    category = Column(String(50), nullable=False)  # 'US Stock', 'International Stock', 'Bond'
    ticker = Column(String(10), nullable=False)
    name = Column(String(100))
    expense_ratio = Column(Float)
    
    # Relationship
    portfolio = relationship('Portfolio', back_populates='fund_selections')
    
    def __repr__(self):
        return f"<FundSelection(portfolio_id={self.portfolio_id}, category='{self.category}', ticker='{self.ticker}')>"


class SavedCalculation(Base):
    __tablename__ = 'saved_calculations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100), nullable=False)
    calculation_type = Column(String(50), nullable=False)  # 'compound_growth', 'fee_impact', etc.
    params = Column(Text)  # JSON string of parameters
    result = Column(Text)  # JSON string of results
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<SavedCalculation(name='{self.name}', calculation_type='{self.calculation_type}')>"


# Create a database engine
def get_engine():
    """Get SQLAlchemy engine using the database URL from environment variables"""
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # Ensure the URL starts with postgresql:// instead of postgres://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        return create_engine(db_url)
    else:
        raise EnvironmentError("DATABASE_URL environment variable not set")


def init_db():
    """Initialize the database by creating all tables"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine


def get_session():
    """Get a database session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


# Portfolio CRUD operations
def save_portfolio(portfolio_obj, user_id=1):
    """
    Save a portfolio object to the database
    
    Args:
        portfolio_obj: A Portfolio object from utils/portfolio.py
        user_id: User ID (default: 1 for single-user mode)
        
    Returns:
        Portfolio: Database portfolio object
    """
    session = get_session()
    
    try:
        # Check if user exists, create if not
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            user = User(id=user_id, username=f"user{user_id}", email=f"user{user_id}@example.com")
            session.add(user)
        
        # Convert portfolio object to database model
        portfolio_data = portfolio_obj.to_dict()
        
        # Create portfolio with proper field mapping
        db_portfolio = Portfolio(
            name=portfolio_data.get('name', 'My Portfolio'),
            user_id=user_id,
            initial_investment=portfolio_data.get('initial_investment', 10000),
            monthly_contribution=portfolio_data.get('monthly_contribution', 500),
            years_to_grow=portfolio_data.get('years_to_grow', 30)
        )
        session.add(db_portfolio)
        session.flush()  # Get the ID
        
        # Create allocation
        allocation = Allocation(
            portfolio_id=db_portfolio.id,
            us_stock=portfolio_data.get('us_stock_allocation', 60),
            international_stock=portfolio_data.get('international_stock_allocation', 30),
            bond=portfolio_data.get('bond_allocation', 10)
        )
        session.add(allocation)
        
        # Add fund selections
        # Create fund selection for US Stock
        us_stock_fund = FundSelection(
            portfolio_id=db_portfolio.id,
            category='US Stock',
            ticker=portfolio_data.get('us_stock_fund', 'VTI'),
            name='',  # Will be filled later
            expense_ratio=0.0  # Will be filled later
        )
        session.add(us_stock_fund)
        
        # Create fund selection for International Stock
        intl_stock_fund = FundSelection(
            portfolio_id=db_portfolio.id,
            category='International Stock',
            ticker=portfolio_data.get('international_stock_fund', 'VXUS'),
            name='',  # Will be filled later
            expense_ratio=0.0  # Will be filled later
        )
        session.add(intl_stock_fund)
        
        # Create fund selection for Bond
        bond_fund = FundSelection(
            portfolio_id=db_portfolio.id,
            category='Bond',
            ticker=portfolio_data.get('bond_fund', 'BND'),
            name='',  # Will be filled later
            expense_ratio=0.0  # Will be filled later
        )
        session.add(bond_fund)
        
        # Commit changes to database
        session.commit()
        
        # Detach the portfolio object from the session to avoid errors
        session.expunge(db_portfolio)
        
        return db_portfolio
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def load_portfolio(portfolio_id, user_id=1):
    """
    Load a portfolio from the database
    
    Args:
        portfolio_id: Portfolio ID
        user_id: User ID (default: 1 for single-user mode)
        
    Returns:
        dict: Portfolio data in a format compatible with utils/portfolio.py
    """
    session = get_session()
    
    try:
        # Get portfolio
        db_portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not db_portfolio:
            return None
        
        # Get allocation
        allocation = session.query(Allocation).filter_by(portfolio_id=portfolio_id).first()
        
        # Get fund selections
        fund_selections = session.query(FundSelection).filter_by(portfolio_id=portfolio_id).all()
        
        # Convert to dict format for Portfolio class
        portfolio_data = {
            'name': db_portfolio.name,
            'initial_investment': db_portfolio.initial_investment,
            'monthly_contribution': db_portfolio.monthly_contribution,
            'years_to_grow': db_portfolio.years_to_grow,
            'us_stock': allocation.us_stock if allocation else 60,
            'international_stock': allocation.international_stock if allocation else 30,
            'bond': allocation.bond if allocation else 10,
            'funds': {}
        }
        
        # Add funds
        for fund in fund_selections:
            portfolio_data['funds'][fund.category] = {
                'ticker': fund.ticker,
                'name': fund.name,
                'expense_ratio': fund.expense_ratio
            }
        
        return portfolio_data
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_user_portfolios(user_id=1):
    """
    Get a list of portfolios for a user
    
    Args:
        user_id: User ID (default: 1 for single-user mode)
        
    Returns:
        list: List of portfolio dicts with id and name
    """
    session = get_session()
    
    try:
        portfolios = session.query(Portfolio).filter_by(user_id=user_id).all()
        return [{'id': p.id, 'name': p.name} for p in portfolios]
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_portfolio(portfolio_id, user_id=1):
    """
    Delete a portfolio
    
    Args:
        portfolio_id: Portfolio ID
        user_id: User ID (default: 1 for single-user mode)
        
    Returns:
        bool: Success flag
    """
    session = get_session()
    
    try:
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if portfolio:
            # Delete related allocations and fund selections (cascade)
            session.delete(portfolio)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()