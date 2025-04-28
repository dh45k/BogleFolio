import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Initialize OpenAI client with error handling
try:
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        logger.warning("OpenAI API key not found in environment variables")
        client = None
    else:
        client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized successfully")
except ImportError:
    logger.error("Failed to import OpenAI module")
    client = None
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {e}")
    client = None

# System message for investment advisor
INVESTMENT_ADVISOR_SYSTEM_MESSAGE = """
You are a helpful financial advisor specializing in Boglehead investment principles. 
You provide guidance on passive investing, low-cost index funds, and long-term investment strategies.

Key principles to adhere to:
1. Emphasize long-term investing over short-term trading
2. Always recommend low-cost index funds (expense ratios < 0.2%)
3. Focus on proper asset allocation based on age and risk tolerance
4. Advocate for tax-efficient placement of investments
5. Recommend diversification across US stocks, international stocks, and bonds
6. Promote the 3-fund portfolio approach: Total US Stock Market, Total International Stock Market, and Total Bond Market
7. Highlight importance of staying the course during market downturns
8. Discourage market timing and individual stock picking

Your advice should be educational, balanced, and focused on helping users become better investors.
Never recommend complicated investment products or high-cost actively managed funds.

Common fund recommendations:
- US Total Market: VTI, ITOT, SCHB, FSKAX
- International: VXUS, IXUS, SCHF, FTIHX
- Bonds: BND, AGG, SCHZ, FXNAX
"""

def get_chatbot_response(messages, include_system_message=True):
    """
    Get a response from the chatbot.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        include_system_message: Whether to include the system message
        
    Returns:
        String response from the chatbot
    """
    if client is None:
        return "Sorry, the AI Assistant is currently unavailable. Please check your OpenAI API key."
        
    try:
        if include_system_message:
            full_messages = [
                {"role": "system", "content": INVESTMENT_ADVISOR_SYSTEM_MESSAGE}
            ] + messages
        else:
            full_messages = messages
            
        response = client.chat.completions.create(
            model=MODEL,
            messages=full_messages,
            temperature=0.7,
            max_tokens=800,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in get_chatbot_response: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

def get_fund_comparison(fund_info):
    """
    Generate a comparison analysis of the provided funds.
    
    Args:
        fund_info: Dictionary containing details about the funds to compare
    
    Returns:
        String analysis from the chatbot
    """
    if client is None:
        return "Sorry, the Fund Comparison tool is currently unavailable. Please check your OpenAI API key."
        
    try:
        prompt = f"""
        Please compare these investment funds and provide a concise analysis:
        
        {fund_info}
        
        Focus on:
        1. Expense ratios and their long-term impact
        2. Performance differences and whether they're statistically significant
        3. Tax efficiency considerations
        4. Tracking error to their benchmarks
        5. Recommendation based on Boglehead principles
        
        Favor the fund with the lowest expense ratio unless there's a compelling reason not to.
        """
        
        messages = [{"role": "user", "content": prompt}]
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": INVESTMENT_ADVISOR_SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in get_fund_comparison: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

def get_allocation_advice(age, risk_tolerance, financial_situation):
    """
    Generate asset allocation advice based on user details.
    
    Args:
        age: User's age
        risk_tolerance: Risk tolerance (low, medium, high)
        financial_situation: Brief description of financial situation
    
    Returns:
        String advice from the chatbot
    """
    if client is None:
        return "Sorry, the Asset Allocation Advisor is currently unavailable. Please check your OpenAI API key."
        
    try:
        prompt = f"""
        Please recommend an asset allocation for someone with these characteristics:
        
        Age: {age}
        Risk Tolerance: {risk_tolerance}
        Financial Situation: {financial_situation}
        
        Provide:
        1. Recommended allocation percentages for US stocks, international stocks, and bonds
        2. Brief explanation of the reasoning
        3. Suggested funds that match this allocation
        4. Any tax-efficient placement considerations
        """
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": INVESTMENT_ADVISOR_SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in get_allocation_advice: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"