import streamlit as st
import yfinance
import json

if 'total_current_value_equity' not in st.session_state:
    st.session_state['total_current_value_equity'] = 0.0
if 'total_invested_value_equity' not in st.session_state:
    st.session_state['total_invested_value_equity'] = 0.0

@st.dialog('Please wait for few seconds...')
def load_equity():
    with st.spinner('Loading values...'):
        with open("data/portfolio.json", "r") as file:
            portfolio_data = json.load(file)
        st.session_state['total_current_value_equity'] = 0.0
        st.session_state['total_invested_value_equity'] = 0.0
        try:
            for row in portfolio_data["equity"]:
                n_stocks = portfolio_data['equity'][row]["no. of shares"]
                try:
                    current_price = yfinance.Ticker(ticker=row).info['currentPrice']
                except:
                    current_price = yfinance.Ticker(ticker=row).info['previousClose']
                current_value = n_stocks * current_price
                invested_price = portfolio_data['equity'][row]["invested price"]
                invested_value = n_stocks * invested_price
                st.session_state['total_current_value_equity'] += current_value
                st.session_state['total_invested_value_equity'] += invested_value
            st.success('Loaded successfully...')
        except Exception as e:
            st.error(str(e))

st.set_page_config(layout="wide")

st.title('Personal Finance - Dashboard')

load_equity()
with st.container(border=True):
    st.write('EQUITIES:')
    st.write(f"CURRENT VALUE: {st.session_state['total_current_value_equity']}")
    st.write(f"INVESTED VALUE: {st.session_state['total_invested_value_equity']}")
    st.write(f"OVERALL PROFIT/ LOSS: {st.session_state['total_current_value_equity'] - st.session_state['total_invested_value_equity']}")
    st.write(f"OVERALL PROFIT/ LOSS %: {(st.session_state['total_current_value_equity'] - st.session_state['total_invested_value_equity'])/st.session_state['total_invested_value_equity']*100.0}")
