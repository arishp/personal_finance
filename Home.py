import streamlit as st
import yfinance

st.title('Personal Finance - Dash board')
ticker = st.text_input(label='ticker', value='infy')
stock_info = yfinance.Ticker(ticker=ticker).info

st.text(stock_info['currentPrice'])

for item in stock_info:
    st.write(f'{item}: {stock_info[item]}')