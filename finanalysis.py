import yfinance as yf
import pandas as pd
import streamlit as st

def fetch_data(tickers, start_date, end_date):
    data_frames = []
    for ticker in tickers:
        stock_data = yf.download(ticker, start=start_date, end=end_date)['Close']
        data_frames.append(stock_data)
    
    data = pd.concat(data_frames, axis=1, keys=tickers)
    data.columns = tickers
    return data

st.title("Financial Analysis Web App")

# User inputs
tickers = st.text_input("Enter stock tickers (comma separated)", "AAPL, MSFT, GOOG").split(",")
tickers = [ticker.strip() for ticker in tickers]
start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2023-01-01"))

# Fetch stock data
stock_data = fetch_data(tickers, start_date, end_date)
returns_data = stock_data.pct_change().dropna()

# Visualizations
st.subheader("Stock Prices")
st.line_chart(stock_data)

st.subheader("Stock Returns")
st.line_chart(returns_data)
