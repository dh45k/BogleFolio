import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import norm

def run_monte_carlo_simulation(initial_investment, monthly_contribution, years, 
                               expected_return, volatility, simulations=1000, 
                               confidence_intervals=[0.05, 0.25, 0.5, 0.75, 0.95]):
    """
    Run a Monte Carlo simulation for retirement planning
    
    Parameters:
    - initial_investment: Initial portfolio value
    - monthly_contribution: Monthly contribution amount
    - years: Number of years to simulate
    - expected_return: Annual expected return (decimal)
    - volatility: Annual volatility/standard deviation (decimal)
    - simulations: Number of simulation paths to generate
    - confidence_intervals: List of confidence intervals to calculate
    
    Returns:
    - Dictionary containing simulation results
    """
    # Convert annual figures to monthly
    monthly_return = expected_return / 12
    monthly_volatility = volatility / np.sqrt(12)
    
    # Total number of months
    months = years * 12
    
    # Initialize array for simulation results
    simulation_results = np.zeros((months + 1, simulations))
    
    # Set initial investment for all simulations
    simulation_results[0, :] = initial_investment
    
    # Run simulations
    for sim in range(simulations):
        # Generate random monthly returns
        random_returns = np.random.normal(monthly_return, monthly_volatility, months)
        
        # Calculate cumulative portfolio value
        for month in range(1, months + 1):
            # Previous month's value
            prev_value = simulation_results[month - 1, sim]
            
            # Current month's growth
            growth = prev_value * (1 + random_returns[month - 1])
            
            # Add monthly contribution
            if month < months:  # Only add contributions before the final month
                current_value = growth + monthly_contribution
            else:
                current_value = growth
                
            simulation_results[month, sim] = current_value
    
    # Create time points (in years)
    time_points = np.linspace(0, years, months + 1)
    
    # Calculate statistics for each time point
    median_values = np.median(simulation_results, axis=1)
    mean_values = np.mean(simulation_results, axis=1)
    
    # Calculate percentiles for confidence intervals
    percentiles = {}
    for ci in confidence_intervals:
        percentiles[ci] = np.percentile(simulation_results, ci * 100, axis=1)
    
    # Final portfolio value statistics
    final_values = simulation_results[-1, :]
    final_mean = np.mean(final_values)
    final_median = np.median(final_values)
    final_min = np.min(final_values)
    final_max = np.max(final_values)
    
    # Calculate probability of reaching various targets
    targets = {}
    target_amounts = [
        initial_investment * 2,  # Double initial investment
        initial_investment * 5,  # 5x initial investment
        1000000,  # $1 million
        2000000,  # $2 million
        5000000   # $5 million
    ]
    
    for target in target_amounts:
        probability = np.mean(final_values >= target) * 100
        targets[f"${target:,.0f}"] = probability
    
    # Calculate safe withdrawal rates
    # Common 4% rule and some variations
    withdrawal_rates = {
        "3%": 0.03 / 12,
        "3.5%": 0.035 / 12,
        "4%": 0.04 / 12,
        "4.5%": 0.045 / 12,
        "5%": 0.05 / 12
    }
    
    # Calculate monthly income for different withdrawal rates
    monthly_income = {}
    for rate_name, rate in withdrawal_rates.items():
        monthly_income[rate_name] = {
            "Median": final_median * rate,
            "Mean": final_mean * rate,
            "Low (5th percentile)": percentiles[0.05][-1] * rate,
            "High (95th percentile)": percentiles[0.95][-1] * rate
        }
    
    # Prepare return data
    results = {
        "simulation_data": {
            "time_points": time_points,
            "simulations": simulation_results,
            "median": median_values,
            "mean": mean_values,
            "percentiles": percentiles
        },
        "statistics": {
            "final_mean": final_mean,
            "final_median": final_median,
            "final_min": final_min,
            "final_max": final_max,
            "target_probabilities": targets,
            "monthly_income": monthly_income
        }
    }
    
    return results

def generate_monte_carlo_plot(simulation_results, scenario_name="Default Scenario"):
    """
    Generate an interactive Plotly plot from Monte Carlo simulation results
    
    Parameters:
    - simulation_results: Results from run_monte_carlo_simulation
    - scenario_name: Name of the scenario for the plot title
    
    Returns:
    - Plotly figure object
    """
    sim_data = simulation_results["simulation_data"]
    time_points = sim_data["time_points"]
    
    fig = go.Figure()
    
    # Add a sample of individual simulation paths (max 50 for performance)
    num_sims = min(50, sim_data["simulations"].shape[1])
    for i in range(num_sims):
        show_legend = True if i == 0 else False
        fig.add_trace(go.Scatter(
            x=time_points,
            y=sim_data["simulations"][:, i],
            mode='lines',
            line=dict(color='rgba(100, 100, 100, 0.1)'),
            name='Simulation Paths',
            showlegend=show_legend,
            hoverinfo='skip'
        ))
    
    # Add percentile ranges
    percentiles = sim_data["percentiles"]
    
    # 5th to 95th percentile range (90% confidence interval)
    fig.add_trace(go.Scatter(
        x=np.concatenate([time_points, time_points[::-1]]),
        y=np.concatenate([percentiles[0.05], percentiles[0.95][::-1]]),
        fill='toself',
        fillcolor='rgba(0, 100, 80, 0.2)',
        line=dict(color='rgba(0, 100, 80, 0)'),
        name='90% Confidence Range',
        showlegend=True
    ))
    
    # 25th to 75th percentile range (50% confidence interval)
    fig.add_trace(go.Scatter(
        x=np.concatenate([time_points, time_points[::-1]]),
        y=np.concatenate([percentiles[0.25], percentiles[0.75][::-1]]),
        fill='toself',
        fillcolor='rgba(0, 100, 80, 0.4)',
        line=dict(color='rgba(0, 100, 80, 0)'),
        name='50% Confidence Range',
        showlegend=True
    ))
    
    # Add median line
    fig.add_trace(go.Scatter(
        x=time_points,
        y=sim_data["median"],
        mode='lines',
        line=dict(color='rgb(0, 100, 80)', width=2, dash='solid'),
        name='Median Outcome',
        showlegend=True
    ))
    
    # Add mean line
    fig.add_trace(go.Scatter(
        x=time_points,
        y=sim_data["mean"],
        mode='lines',
        line=dict(color='rgb(200, 120, 0)', width=2, dash='dash'),
        name='Mean Outcome',
        showlegend=True
    ))
    
    # Update layout
    fig.update_layout(
        title=f'Monte Carlo Simulation: {scenario_name}',
        xaxis_title='Years',
        yaxis_title='Portfolio Value ($)',
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
    
    return fig

def calculate_success_rates(simulation_results, withdrawal_amounts):
    """
    Calculate retirement success rates based on various monthly withdrawal amounts
    
    Parameters:
    - simulation_results: Results from run_monte_carlo_simulation
    - withdrawal_amounts: List of monthly withdrawal amounts to test
    
    Returns:
    - DataFrame with success rates
    """
    final_values = simulation_results["simulation_data"]["simulations"][-1, :]
    
    success_rates = []
    for amount in withdrawal_amounts:
        # Calculate required principal for this withdrawal using the 4% rule
        # (Monthly withdrawal × 12 months) / 0.04 = required principal
        required_principal = (amount * 12) / 0.04
        
        # Calculate percentage of simulations where final value exceeds required amount
        success_rate = np.mean(final_values >= required_principal) * 100
        
        success_rates.append({
            'Monthly Withdrawal': amount,
            'Annual Withdrawal': amount * 12,
            'Required Principal (4% Rule)': required_principal,
            'Success Rate (%)': success_rate
        })
    
    return pd.DataFrame(success_rates)

def calculate_retirement_readiness(target_monthly_income, simulation_results, withdrawal_rate=0.04):
    """
    Calculate retirement readiness metrics
    
    Parameters:
    - target_monthly_income: Desired monthly income in retirement
    - simulation_results: Results from run_monte_carlo_simulation
    - withdrawal_rate: Annual withdrawal rate (default 4%)
    
    Returns:
    - Dictionary with retirement readiness metrics
    """
    # Calculate required nest egg based on 4% rule
    required_principal = (target_monthly_income * 12) / withdrawal_rate
    
    # Get final portfolio values from simulations
    final_values = simulation_results["simulation_data"]["simulations"][-1, :]
    
    # Calculate success rate
    success_rate = np.mean(final_values >= required_principal) * 100
    
    # Calculate percentage of target income likely to be achieved
    percentiles = {
        "5th Percentile": np.percentile(final_values, 5) * (withdrawal_rate / 12),
        "Median": np.percentile(final_values, 50) * (withdrawal_rate / 12),
        "Mean": np.mean(final_values) * (withdrawal_rate / 12),
        "95th Percentile": np.percentile(final_values, 95) * (withdrawal_rate / 12)
    }
    
    income_percentages = {
        key: (value / target_monthly_income) * 100 for key, value in percentiles.items()
    }
    
    # Calculate years to retirement
    # Simplified calculation assuming current contributions continue
    median_data = simulation_results["simulation_data"]["median"]
    time_points = simulation_results["simulation_data"]["time_points"]
    
    # Find where median crosses the required principal threshold
    retirement_ready_index = np.where(median_data >= required_principal)[0]
    
    if len(retirement_ready_index) > 0:
        years_to_retirement = time_points[retirement_ready_index[0]]
    else:
        years_to_retirement = float('inf')  # Not achieved within simulation timeframe
    
    return {
        "target_monthly_income": target_monthly_income,
        "required_principal": required_principal,
        "success_rate": success_rate,
        "monthly_income_projections": percentiles,
        "income_percentage_of_target": income_percentages,
        "years_to_retirement": years_to_retirement
    }