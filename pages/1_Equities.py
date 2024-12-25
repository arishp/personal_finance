import streamlit as st
import yfinance
import json

if 'total_current_value_equity' not in st.session_state:
    st.session_state['total_current_value_equity'] = 0.0
if 'total_invested_value_equity' not in st.session_state:
    st.session_state['total_invested_value_equity'] = 0.0

st.set_page_config(layout="wide")

st.title('Personal Finance - Equities')

with open("data/portfolio.json", "r") as file:
    portfolio_data = json.load(file)

equity_titles = st.columns(8)
with equity_titles[0]:
    st.text('Stock name')
with equity_titles[1]:
    st.text('No. of stocks')
with equity_titles[2]:
    st.text('Current price')
with equity_titles[3]:
    st.text('Current value')
with equity_titles[4]:
    st.text('Invested price')
with equity_titles[5]:
    st.text('Invested value')
with equity_titles[6]:
    st.text('Profit/ Loss value')
with equity_titles[7]:
    st.text('Profit/ Loss %')


st.session_state['total_current_value_equity'] = 0.0
st.session_state['total_invested_value_equity'] = 0.0
try:
    for row in portfolio_data["equity"]:

        stock_name = row
        n_stocks = portfolio_data['equity'][row]["no. of shares"]
        try:
            current_price = yfinance.Ticker(ticker=row).info['currentPrice']
        except:
            current_price = yfinance.Ticker(ticker=row).info['previousClose']
        current_value = n_stocks * current_price
        invested_price = portfolio_data['equity'][row]["invested price"]
        invested_value = n_stocks * invested_price
        profit_loss = current_value - invested_value
        pl_percent = profit_loss/invested_value*100.00

        st.session_state['total_current_value_equity'] += current_value
        st.session_state['total_invested_value_equity'] += invested_value

        equity_values = st.columns(8)

        with equity_values[0]:
            st.text_input(value=stock_name, key=f'stock_name_{row}', label='stock_name', label_visibility='collapsed', disabled=True)
        with equity_values[1]:
            portfolio_data['equity'][row]["no. of shares"] = st.number_input(value=n_stocks, key=f'n_stocks_{row}', label='n_stocks', 
                                                                            label_visibility='collapsed')
        with equity_values[2]:
            st.number_input(value=current_price, key=f'curr_price_{row}', label='current_price', label_visibility='collapsed', disabled=True)
        with equity_values[3]:
            st.number_input(value=current_value, key=f'curr_value_{row}', label='current_value', label_visibility='collapsed', disabled=True,
                        format="%.2f")
        with equity_values[4]:
            portfolio_data['equity'][row]["invested price"] = st.number_input(value=invested_price, key=f'inv_price_{row}', 
                                                                            label='invested_price', label_visibility='collapsed', step=0.01)
        with equity_values[5]:
            st.number_input(value=invested_value, key=f'inv_value_{row}', label='invested_value', label_visibility='collapsed', disabled=True,
                        format="%.2f")
        with equity_values[6]:
            st.number_input(value=profit_loss, key=f'profit_loss_{row}', label='profit_loss', label_visibility='collapsed', disabled=True,
                        format="%.2f")
        with equity_values[7]:
            st.number_input(value=pl_percent, key=f'pl_percent_{row}', label='pl_percent', label_visibility='collapsed', disabled=True,
                        format="%.2f")

        with open("data/portfolio.json", "w") as file:
            json.dump(portfolio_data, file, indent=4)
except Exception as e:
    st.write(str(e))
    
st.write(f"CURRENT VALUE: {st.session_state['total_current_value_equity']}")
st.write(f"INVESTED VALUE: {st.session_state['total_invested_value_equity']}")
st.write(f"OVERALL PROFIT/ LOSS: {st.session_state['total_current_value_equity'] - st.session_state['total_invested_value_equity']}")
st.write(f"OVERALL PROFIT/ LOSS %: {(st.session_state['total_current_value_equity'] - st.session_state['total_invested_value_equity'])/st.session_state['total_invested_value_equity']*100.0}")
yfinance.Ticker(ticker='are&m.ns').info

# ticker = st.text_input(label='ticker', value='infy')
# stock_info = yfinance.Ticker(ticker=ticker).info

# st.text(stock_info['currentPrice'])

# for item in stock_info:
#     st.write(f'{item}: {stock_info[item]}')