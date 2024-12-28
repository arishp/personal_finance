import streamlit as st
import yfinance
import json

################################## FUNCTION DEFINITIONS ################################################################

# initialize session state
def initialize_session_state():
    # initialize total equity investment and current value
    if 'total_current_value_equity' not in st.session_state:
        st.session_state['total_current_value_equity'] = 0.0
    if 'total_invested_value_equity' not in st.session_state:
        st.session_state['total_invested_value_equity'] = 0.0
    if 'equity_column_headers' not in st.session_state:
        st.session_state['equity_column_headers'] = ['Stock name', 'No. of stocks', 'Invested price', 'Invested value', 'Current price', 
                                                     'Current value', 'Profit/ Loss value', 'Profit/ Loss %']
    if 'equity_page_count' not in st.session_state:
        st.session_state['equity_page_count'] = 0

# display column headers
def display_column_header():
    with column_header_container.container(border=True):
        equity_titles = st.columns(len(st.session_state['equity_column_headers']))
        for i in range(len(st.session_state['equity_column_headers'])):
            with equity_titles[i]:
                st.text(st.session_state['equity_column_headers'][i])

def load_equity_page():
    st.session_state['total_invested_value_equity'] = 0.0
    st.session_state['total_current_value_equity'] = 0.0
    # read portfolio file
    with open("data/portfolio.json", "r") as file:
        portfolio_data = json.load(file)
    # display details of all stocks        
    try:
        with stock_values_container.container(border=True, height=400):
            # for each stock in the portfolio
            for row in portfolio_data["equity"]:
                stock_name = row
                n_stocks = portfolio_data['equity'][row]["no. of shares"] # no. of stocks
                invested_price = portfolio_data['equity'][row]["invested price"] # invested price per share of a stock
                invested_value = n_stocks * invested_price
                current_price = portfolio_data['equity'][row]["current price"] # current price per share of a stock
                current_value = n_stocks * current_price
                pl_value = current_value - invested_value # profit or loss value
                pl_percent = pl_value/invested_value*100.00
                st.session_state['total_invested_value_equity'] += invested_value # total invested value
                st.session_state['total_current_value_equity'] += current_value # total current value
                # display values
                equity_values = st.columns(len(st.session_state['equity_column_headers']))
                with equity_values[0]:
                    st.text_input(value=stock_name, key=f'stock_name_{row}_load', label='stock_name', 
                                  label_visibility='collapsed', disabled=True)
                with equity_values[1]:
                    portfolio_data['equity'][row]["no. of shares"] = st.number_input(value=n_stocks, key=f'n_stocks_{row}_load', 
                                                                                     label='n_stocks', label_visibility='collapsed')
                with equity_values[2]:
                    portfolio_data['equity'][row]["invested price"] = st.number_input(value=invested_price, key=f'inv_price_{row}_load', 
                                                                                      label='invested_price', label_visibility='collapsed', step=0.01)
                with equity_values[3]:
                    st.number_input(value=invested_value, key=f'inv_value_{row}_load', label='invested_value', 
                                    label_visibility='collapsed', disabled=True, format="%.2f")
                with equity_values[4]:
                    portfolio_data['equity'][row]["current price"] = st.number_input(value=current_price, key=f'curr_price_{row}_load', 
                                                                                    label='current_price', label_visibility='collapsed', 
                                                                                    disabled=True)
                with equity_values[5]:
                    st.number_input(value=current_value, key=f'curr_value_{row}_load', label='current_value', 
                                    label_visibility='collapsed', disabled=True, format="%.2f")
                with equity_values[6]:
                    st.number_input(value=pl_value, key=f'profit_loss_{row}_load', label='profit_loss', 
                                    label_visibility='collapsed', disabled=True, format="%.2f")
                with equity_values[7]:
                    st.number_input(value=pl_percent, key=f'pl_percent_{row}_load', label='pl_percent', 
                                    label_visibility='collapsed', disabled=True, format="%.2f")
                with open("data/portfolio.json", "w") as file:
                    json.dump(portfolio_data, file, indent=4)
    except Exception as e:
        st.write(str(e))

def refresh_equity_values():
    st.session_state['total_invested_value_equity'] = 0.0
    st.session_state['total_current_value_equity'] = 0.0
    # read portfolio file
    with open("data/portfolio.json", "r") as file:
        portfolio_data = json.load(file)
    # display details of all stocks        
    try:
        with stock_values_container.container(border=True, height=400):
            # for each stock in the portfolio
            for row in portfolio_data["equity"]:
                stock_name = row
                n_stocks = portfolio_data['equity'][row]["no. of shares"] # no. of stocks
                invested_price = portfolio_data['equity'][row]["invested price"] # invested price per share of a stock
                invested_value = n_stocks * invested_price
                try:
                    current_price = yfinance.Ticker(ticker=row).info['currentPrice']
                except:
                    current_price = yfinance.Ticker(ticker=row).info['previousClose'] # current price per share of a stock
                current_value = n_stocks * current_price
                pl_value = current_value - invested_value # profit or loss value
                pl_percent = pl_value/invested_value*100.00
                st.session_state['total_invested_value_equity'] += invested_value # total invested value
                st.session_state['total_current_value_equity'] += current_value # total current value
                # display values
                equity_values = st.columns(len(st.session_state['equity_column_headers']))
                with equity_values[0]:
                    st.text_input(value=stock_name, key=f'stock_name_{row}', label='stock_name', label_visibility='collapsed', disabled=True)
                with equity_values[1]:
                    portfolio_data['equity'][row]["no. of shares"] = st.number_input(value=n_stocks, key=f'n_stocks_{row}', label='n_stocks', 
                                                                                    label_visibility='collapsed')
                with equity_values[2]:
                    portfolio_data['equity'][row]["invested price"] = st.number_input(value=invested_price, key=f'inv_price_{row}', 
                                                                                    label='invested_price', label_visibility='collapsed', 
                                                                                    step=0.01)
                with equity_values[3]:
                    st.number_input(value=invested_value, key=f'inv_value_{row}', label='invested_value', label_visibility='collapsed', 
                                    disabled=True, format="%.2f")
                with equity_values[4]:
                    portfolio_data['equity'][row]["current price"] = st.number_input(value=current_price, key=f'curr_price_{row}', 
                                                                                    label='current_price', label_visibility='collapsed', 
                                                                                    disabled=True)
                with equity_values[5]:
                    st.number_input(value=current_value, key=f'curr_value_{row}', label='current_value', label_visibility='collapsed', 
                                    disabled=True, format="%.2f")
                with equity_values[6]:
                    st.number_input(value=pl_value, key=f'profit_loss_{row}', label='profit_loss', label_visibility='collapsed', 
                                    disabled=True, format="%.2f")
                with equity_values[7]:
                    st.number_input(value=pl_percent, key=f'pl_percent_{row}', label='pl_percent', label_visibility='collapsed', 
                                    disabled=True, format="%.2f")
                with open("data/portfolio.json", "w") as file:
                    json.dump(portfolio_data, file, indent=4)
    except Exception as e:
        st.write(str(e))

def display_consolidation():
    with consolidated_container.container(border=True):
        st.write("**Consolidated values:**")
        st.write(f'Total invested value: {st.session_state["total_invested_value_equity"]}')
        st.write(f'Total current value: {st.session_state["total_current_value_equity"]}')
        txt = "Total profit/ loss value: {:.2f}"
        st.write(txt.format((st.session_state["total_current_value_equity"]-st.session_state["total_invested_value_equity"])))
        txt = "Total profit/ loss percentage: {:.2f}"
        st.write(txt.format((st.session_state["total_current_value_equity"]-st.session_state["total_invested_value_equity"])/st.session_state["total_invested_value_equity"]*100.0))

########################################################################################################################

st.set_page_config(layout="wide")

st.title('Personal Finance - Equities')

refresh_button_placeholder = st.empty()
column_header_container = st.empty()
stock_values_container = st.empty()
consolidated_container = st.empty()

initialize_session_state()

with refresh_button_placeholder:
    if st.button('Refresh values'):
        refresh_equity_values()

display_column_header()

load_equity_page()

display_consolidation()    

# yfinance.Ticker(ticker='goldbees.ns').info

# ticker = st.text_input(label='ticker', value='infy')
# stock_info = yfinance.Ticker(ticker=ticker).info

# st.text(stock_info['currentPrice'])

# for item in stock_info:
#     st.write(f'{item}: {stock_info[item]}')