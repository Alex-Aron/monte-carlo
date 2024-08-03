import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

# Function to simulate the price of an option using Monte Carlo
def monte_carlo_option_pricing(S0, K, T, r, sigma, num_simulations, num_steps):
    dt = T / num_steps
    prices = np.zeros((num_steps + 1, num_simulations))
    prices[0] = S0

    for t in range(1, num_steps + 1):
        Z = np.random.standard_normal(num_simulations)
        prices[t] = prices[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)

    return prices
def main():
    # Streamlit UI
    st.title('Monte Carlo Option Pricing')

    # Radio button for input method
    input_method = st.radio("Choose input method:", ("Manual Input", "Select Stock"))

    if input_method == "Manual Input":
        S0 = st.number_input('Initial stock price (S0)', value=100.0)
    else:
        stock_ticker = st.text_input("Enter Stock Ticker", value="AAPL")
        period = st.selectbox("Select Time Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "10y", "ytd", "max"])
        #Make sure that the stock ticker is valid if the user selects the stock option
        try:
            stock_data = yf.Ticker(stock_ticker)
            S0 = stock_data.history(period=period)['Close'][0]
        except:
            st.warning("Please enter a valid stock ticker")
            st.stop()
        st.write(f"Stock price of {stock_ticker} for period '{period}': {S0:.2f}")

    # Default strike price set to 5% above the initial stock price(I think this is reasonable)
    K = st.number_input('Strike price (K)', value=S0 * 1.05)
    T = st.number_input('Time to maturity (T) in years', value=1.0)
    r = st.number_input('Risk-free rate (r)', value=0.05)
    sigma = st.number_input('Volatility (sigma)', value=0.2)
    num_simulations = st.number_input('Number of simulations', value=1000, step=100)
    num_steps = st.number_input('Number of time steps', value=100, step=10)

    if st.button('Run Simulation'):
        prices = monte_carlo_option_pricing(S0, K, T, r, sigma, num_simulations, num_steps)
        
        # Calculate the option price
        option_price = np.exp(-r * T) * np.mean(np.maximum(prices[-1] - K, 0))
        st.write(f'Option Price: {option_price:.2f}')
        
        # Plot the simulations
        plt.figure(figsize=(10, 6))
        plt.plot(prices[:, :10])  # Plotting only 10 simulations for clarity
        plt.title('Monte Carlo Simulations of Stock Price')
        plt.xlabel('Time Steps')
        plt.ylabel('Stock Price')
        st.pyplot(plt.gcf())

        # Plot the distribution of the final prices
        plt.figure(figsize=(10, 6))
        plt.hist(prices[-1], bins=50, density=True)
        plt.title('Distribution of Final Stock Prices')
        plt.xlabel('Stock Price')
        plt.ylabel('Frequency')
        st.pyplot(plt.gcf())

if __name__ == '__main__':
    main()