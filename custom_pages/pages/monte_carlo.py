import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.monte_carlo import run_monte_carlo_simulation, generate_monte_carlo_plot, calculate_success_rates, calculate_retirement_readiness

def show_monte_carlo_page(portfolio):
    """
    Display the Monte Carlo simulation page for retirement planning
    """
    st.title("Monte Carlo Retirement Simulation")
    
    st.markdown("""
    This tool uses Monte Carlo simulation to project the possible future performance of your portfolio.
    By running thousands of simulations with randomized market returns, we can estimate the range of 
    possible outcomes for your retirement savings.
    """)
    
    # Simulation Parameters Section
    st.subheader("Simulation Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Initial values from portfolio
        initial_investment = st.number_input(
            "Initial Investment ($)", 
            min_value=0, 
            max_value=10000000, 
            value=int(portfolio.initial_investment),
            step=1000,
            format="%d"
        )
        
        monthly_contribution = st.number_input(
            "Monthly Contribution ($)", 
            min_value=0, 
            max_value=100000, 
            value=int(portfolio.monthly_contribution),
            step=100,
            format="%d"
        )
        
        years_to_simulate = st.slider(
            "Years to Simulate", 
            min_value=5, 
            max_value=50, 
            value=min(30, portfolio.years_to_grow),
            step=1
        )
    
    with col2:
        # Default expected return from portfolio, but allow user to adjust
        portfolio_return = portfolio.get_weighted_return()
        expected_return = st.slider(
            "Expected Annual Return (%)", 
            min_value=1.0, 
            max_value=15.0, 
            value=float(portfolio_return),
            step=0.1,
            format="%.1f"
        ) / 100
        
        # Default volatility based on portfolio allocation
        # This is a simplified estimate - stocks ~15-20% volatility, bonds ~5-8%
        stock_allocation = (portfolio.us_stock_allocation + portfolio.international_stock_allocation) / 100
        bond_allocation = portfolio.bond_allocation / 100
        estimated_volatility = (stock_allocation * 0.18) + (bond_allocation * 0.06)
        
        volatility = st.slider(
            "Annual Volatility/Standard Deviation (%)", 
            min_value=1.0, 
            max_value=25.0, 
            value=float(estimated_volatility * 100),
            step=0.5,
            format="%.1f"
        ) / 100
        
        num_simulations = st.select_slider(
            "Number of Simulations",
            options=[100, 500, 1000, 2000, 5000],
            value=1000
        )
    
    # Run simulations button
    if st.button("Run Monte Carlo Simulation"):
        with st.spinner("Running simulations..."):
            # Run the Monte Carlo simulation
            simulation_results = run_monte_carlo_simulation(
                initial_investment=initial_investment,
                monthly_contribution=monthly_contribution,
                years=years_to_simulate,
                expected_return=expected_return,
                volatility=volatility,
                simulations=num_simulations
            )
            
            # Store in session state for reference
            st.session_state.simulation_results = simulation_results
        
        # Show simulation results
        st.subheader("Portfolio Value Projections")
        
        # Generate and display the Monte Carlo plot
        scenario_name = f"{years_to_simulate}-Year Projection (Return: {expected_return:.1%}, Volatility: {volatility:.1%})"
        mc_fig = generate_monte_carlo_plot(simulation_results, scenario_name)
        st.plotly_chart(mc_fig, use_container_width=True)
        
        # Display statistics
        st.subheader("Simulation Statistics")
        stats = simulation_results["statistics"]
        
        # Create columns for key metrics
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(
                "Median Final Value",
                f"${stats['final_median']:,.0f}"
            )
        
        with metric_col2:
            st.metric(
                "Mean Final Value",
                f"${stats['final_mean']:,.0f}"
            )
        
        with metric_col3:
            st.metric(
                "Minimum Final Value",
                f"${stats['final_min']:,.0f}"
            )
        
        with metric_col4:
            st.metric(
                "Maximum Final Value",
                f"${stats['final_max']:,.0f}"
            )
        
        # Target probabilities
        st.subheader("Probability of Reaching Targets")
        
        targets = stats["target_probabilities"]
        target_data = {
            "Target Amount": list(targets.keys()),
            "Probability (%)": list(targets.values())
        }
        target_df = pd.DataFrame(target_data)
        
        # Create bar chart for target probabilities
        fig_targets = go.Figure(go.Bar(
            x=target_df["Target Amount"],
            y=target_df["Probability (%)"],
            marker_color='rgb(26, 118, 255)'
        ))
        
        fig_targets.update_layout(
            title="Probability of Reaching Various Portfolio Targets",
            xaxis_title="Target Portfolio Value",
            yaxis_title="Probability (%)",
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig_targets, use_container_width=True)
        
        # Retirement income section
        st.subheader("Estimated Monthly Retirement Income")
        st.markdown("""
        The table below shows potential monthly income based on different withdrawal rates.
        The traditional "4% rule" suggests you can safely withdraw 4% of your portfolio in the first year,
        then adjust that amount for inflation each year without running out of money over a 30-year retirement.
        """)
        
        # Create a dataframe for the monthly income data
        income_data = []
        for rate, values in stats["monthly_income"].items():
            income_data.append({
                "Withdrawal Rate": rate,
                "Median Monthly Income": f"${values['Median']:,.0f}",
                "Mean Monthly Income": f"${values['Mean']:,.0f}",
                "Low (5th percentile)": f"${values['Low (5th percentile)']:,.0f}",
                "High (95th percentile)": f"${values['High (95th percentile)']:,.0f}"
            })
        
        income_df = pd.DataFrame(income_data)
        st.dataframe(income_df, hide_index=True, use_container_width=True)
        
        # Retirement readiness calculator
        st.subheader("Retirement Readiness Calculator")
        st.markdown("""
        Enter your target monthly income in retirement to see if you're on track.
        """)
        
        target_monthly_income = st.number_input(
            "Target Monthly Income in Retirement ($)",
            min_value=1000,
            max_value=50000,
            value=5000,
            step=500,
            format="%d"
        )
        
        retirement_rate = st.selectbox(
            "Withdrawal Rate Strategy",
            options=["4% (Traditional)", "3.5% (Conservative)", "3% (Very Conservative)"],
            index=0
        )
        
        # Extract the percentage from the selected option
        rate_value = float(retirement_rate.split("%")[0]) / 100
        
        # Calculate retirement readiness
        readiness = calculate_retirement_readiness(
            target_monthly_income=target_monthly_income,
            simulation_results=simulation_results,
            withdrawal_rate=rate_value
        )
        
        # Display retirement readiness metrics
        readiness_col1, readiness_col2 = st.columns(2)
        
        with readiness_col1:
            st.metric(
                "Required Nest Egg",
                f"${readiness['required_principal']:,.0f}"
            )
            
            st.metric(
                "Probability of Success",
                f"{readiness['success_rate']:.1f}%"
            )
            
            if readiness['years_to_retirement'] != float('inf'):
                st.metric(
                    "Estimated Years to Retirement",
                    f"{readiness['years_to_retirement']:.1f} years"
                )
            else:
                st.metric(
                    "Estimated Years to Retirement",
                    "Not within simulation"
                )
        
        with readiness_col2:
            st.metric(
                "Projected Monthly Income (Median)",
                f"${readiness['monthly_income_projections']['Median']:,.0f}",
                f"{readiness['income_percentage_of_target']['Median'] - 100:.1f}% vs target"
            )
            
            st.metric(
                "Projected Monthly Income (Low)",
                f"${readiness['monthly_income_projections']['5th Percentile']:,.0f}",
                f"{readiness['income_percentage_of_target']['5th Percentile'] - 100:.1f}% vs target"
            )
            
            st.metric(
                "Projected Monthly Income (High)",
                f"${readiness['monthly_income_projections']['95th Percentile']:,.0f}",
                f"{readiness['income_percentage_of_target']['95th Percentile'] - 100:.1f}% vs target"
            )
            
        # Safety of various withdrawal amounts
        st.subheader("Success Rates for Different Withdrawal Amounts")
        st.markdown("""
        The table below shows the probability of success for different monthly withdrawal amounts,
        based on the traditional 4% rule.
        """)
        
        # Create percentage of median income values
        median_income = readiness['monthly_income_projections']['Median']
        withdrawal_amounts = [
            median_income * 0.5,   # 50% of median income
            median_income * 0.75,  # 75% of median income
            median_income,         # 100% of median income
            median_income * 1.25,  # 125% of median income
            median_income * 1.5    # 150% of median income
        ]
        
        # Calculate success rates
        success_df = calculate_success_rates(simulation_results, withdrawal_amounts)
        
        # Display the table
        st.dataframe(
            success_df.style.format({
                'Monthly Withdrawal': '${:,.0f}',
                'Annual Withdrawal': '${:,.0f}',
                'Required Principal (4% Rule)': '${:,.0f}',
                'Success Rate (%)': '{:.1f}%'
            }),
            hide_index=True,
            use_container_width=True
        )
        
        # Disclaimer
        st.markdown("""
        ---
        **Disclaimer:** Monte Carlo simulations are based on historical market behavior and assumptions about future returns.
        Actual results may vary significantly. This tool is for educational purposes only and should not be considered financial advice.
        """)
    else:
        st.info("Click 'Run Monte Carlo Simulation' to see retirement projections.")