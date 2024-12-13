import streamlit as st
import yfinance
import json
st.set_page_config(layout="wide")

st.title('Personal Finance - Dash board')

with open("data/portfolio.json", "r") as file:
    portfolio_data = json.load(file)

# for item in portfolio_data['equity']:
#     st.write(portfolio_data['equity'][item]["no of shares"])

stock_name_col, n_stocks_col, curr_price_col, curr_value_col, inv_price_col, inv_value_col = st.columns(6)
with stock_name_col:
    st.text('Stock name')
with n_stocks_col:
    st.text('No. of stocks')
with curr_price_col:
    st.text('Current price')
with curr_value_col:
    st.text('Current value')
with inv_price_col:
    st.text('Invested price')
with inv_value_col:
    st.text('Invested value')

for row in portfolio_data["equity"]:

    stock_name = row
    n_stocks = portfolio_data['equity'][row]["no. of shares"]
    current_price = yfinance.Ticker(ticker=row).info['currentPrice']
    current_value = n_stocks * current_price
    invested_price = portfolio_data['equity'][row]["invested price"]
    invested_value = n_stocks * invested_price

    stock_name_col, n_stocks_col, curr_price_col, curr_value_col, inv_price_col, inv_value_col = st.columns(6)

    with stock_name_col:
        st.text_input(value=stock_name, key=f'stock_name_{row}', label='stock_name', label_visibility='collapsed', disabled=True)
    with n_stocks_col:
        portfolio_data['equity'][row]["no. of shares"] = st.number_input(value=n_stocks, key=f'n_stocks_{row}', label='n_stocks', 
                                                                         label_visibility='collapsed')
    with curr_price_col:
        st.number_input(value=current_price, key=f'curr_price_{row}', label='current_price', label_visibility='collapsed', disabled=True)
    with curr_value_col:
        st.number_input(value=current_value, key=f'curr_value_{row}', label='current_value', label_visibility='collapsed', disabled=True,
                      format="%.2f")
    with inv_price_col:
        portfolio_data['equity'][row]["invested price"] = st.number_input(value=invested_price, key=f'inv_price_{row}', 
                                                                          label='invested_price', label_visibility='collapsed', step=0.01)

    with inv_value_col:
        st.number_input(value=invested_value, key=f'inv_value_{row}', label='invested_value', label_visibility='collapsed', disabled=True,
                      format="%.2f")

    with open("data/portfolio.json", "w") as file:
        json.dump(portfolio_data, file, indent=4)
    
st.rerun()

yfinance.Ticker(ticker='are&m.ns').info

# ticker = st.text_input(label='ticker', value='infy')
# stock_info = yfinance.Ticker(ticker=ticker).info

# st.text(stock_info['currentPrice'])

# for item in stock_info:
#     st.write(f'{item}: {stock_info[item]}')