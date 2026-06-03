import yfinance as yf
import pandas as pd
import streamlit as st
import numpy as np

# Download stock data
def fetch_data(tickers, start_date, end_date):
    data_frames = []

    for ticker in tickers:
        stock_data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )['Close']

        data_frames.append(stock_data)

    data = pd.concat(data_frames, axis=1, keys=tickers)
    data.columns = tickers

    return data


# Annualized Sharpe Ratio
def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    daily_rf = risk_free_rate / 252

    excess_returns = returns - daily_rf

    sharpe_ratios = (
        excess_returns.mean() /
        excess_returns.std()
    ) * np.sqrt(252)

    return sharpe_ratios


# Annualized Sortino Ratio
def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    daily_rf = risk_free_rate / 252

    excess_returns = returns - daily_rf

    downside_returns = excess_returns.where(excess_returns < 0)

    downside_deviation = downside_returns.std()

    sortino_ratios = (
        excess_returns.mean() /
        downside_deviation
    ) * np.sqrt(252)

    return sortino_ratios

def portfolio_optimization(returns):
    return np.ones(len(returns.columns)) / len(returns.columns)


# Streamlit App
st.title("Financial Analysis Web App")

# User inputs
tickers = st.text_input(
    "Enter stock tickers (comma separated)",
    "AAPL, MSFT, GOOG"
).split(",")

tickers = [ticker.strip().upper() for ticker in tickers]

start_date = st.date_input(
    "Start Date",
    pd.to_datetime("2020-01-01")
)

end_date = st.date_input(
    "End Date",
    pd.to_datetime("2023-01-01")
)

risk_free_rate = st.number_input(
    "Annual Risk-Free Rate",
    min_value=0.0,
    max_value=0.20,
    value=0.02,
    step=0.005,
    format="%.3f"
)

# Fetch stock data
stock_data = fetch_data(tickers, start_date, end_date)

# Calculate daily returns
returns_data = stock_data.pct_change().dropna()

# Charts
st.subheader("Stock Prices")
st.line_chart(stock_data)

st.subheader("Daily Returns")
st.line_chart(returns_data)

# Calculate metrics
sharpe_ratios = calculate_sharpe_ratio(
    returns_data,
    risk_free_rate
)

sortino_ratios = calculate_sortino_ratio(
    returns_data,
    risk_free_rate
)

# Display metrics
metrics = pd.DataFrame({
    "Sharpe Ratio": sharpe_ratios,
    "Sortino Ratio": sortino_ratios
})

st.subheader("Performance Metrics")
st.dataframe(metrics.round(3))

# Optional summary statistics
st.subheader("Return Statistics")

summary_stats = pd.DataFrame({
    "Annualized Return (%)":
        returns_data.mean() * 252 * 100,
    "Annualized Volatility (%)":
        returns_data.std() * np.sqrt(252) * 100
})

st.dataframe(summary_stats.round(2))

optimal_weights = portfolio_optimization(returns_data)

st.subheader("Portfolio Optimization")
st.write("Optimal Portfolio Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    st.write(f"{ticker}: {weight:.2%}")

csv_data = stock_data.to_csv()
st.download_button("Download Stock Data CSV", csv_data, "stock_data.csv")
