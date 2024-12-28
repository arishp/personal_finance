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
        st.session_state['equity_column_headers'] = ['Stock name', 'No. of stocks', 'Invested price', 'Current price', 
                                                     'Profit/ Loss', 'Previous close']
    if 'equity_page_count' not in st.session_state:
        st.session_state['equity_page_count'] = 0

# display column headers
def display_column_header():
    with column_header_container.container(border=True):
        equity_titles = st.columns(len(st.session_state['equity_column_headers']))
        for i in range(len(st.session_state['equity_column_headers'])):
            with equity_titles[i]:
                st.write(f"**{st.session_state['equity_column_headers'][i]}**")

def load_equity_page():
    st.session_state['total_invested_value_equity'] = 0.0
    st.session_state['total_current_value_equity'] = 0.0
    # read portfolio file
    with open("data/portfolio.json", "r") as file:
        portfolio_data = json.load(file)
    # display details of all stocks        
    try:
        with stock_values_container.container(border=True, height=600):
            # for each stock in the portfolio
            for row in portfolio_data["equity"]:
                stock_name = row
                n_stocks = portfolio_data['equity'][row]["no. of shares"] # no. of stocks
                invested_price = portfolio_data['equity'][row]["invested price"] # invested price per share of a stock
                invested_value = n_stocks * invested_price
                current_price = portfolio_data['equity'][row]["current price"] # current price per share of a stock
                previous_close = portfolio_data['equity'][row]['previous close']
                prevdiff_value = current_price - previous_close
                prevdiff_percent = prevdiff_value/ previous_close * 100.00
                todaypl_value = prevdiff_value * n_stocks
                current_value = n_stocks * current_price
                pl_price = current_price - invested_price
                pl_value = current_value - invested_value # profit or loss value
                pl_percent = pl_value/invested_value*100.00
                st.session_state['total_invested_value_equity'] += invested_value # total invested value
                st.session_state['total_current_value_equity'] += current_value # total current value
                # display values
                equity_values = st.columns(len(st.session_state['equity_column_headers']))
                with equity_values[0]:
                    st.write(stock_name)
                with equity_values[1]:
                    st.write(f"{n_stocks}")
                with equity_values[2]:
                    st.write(f"Rs. {invested_price}/ share")
                    txt = "Rs. {:.2f}"
                    st.write(txt.format(invested_value))
                with equity_values[3]:
                    st.write(f"Rs. {current_price}/ share")
                    txt = "Rs. {:.2f}"
                    st.write(txt.format(current_value))
                with equity_values[4]:
                    if pl_price > 0.0:
                        txt_pl_price = ":green[Rs. {:.2f}/ share]"
                        txt_pl_value = ":green[Rs. {:.2f} ({:.2f}%)]"
                    else:
                        txt_pl_price = ":red[Rs. {:.2f}/ share]"
                        txt_pl_value = ":red[Rs. {:.2f} ({:.2f}%)]"
                    st.write(txt_pl_price.format(pl_price))
                    st.write(txt_pl_value.format(pl_value, pl_percent))
                with equity_values[5]:
                    if prevdiff_value > 0.0:
                        txt_pl_prev = "Rs. {:.2f} :green[(Rs. {:.2f})]"
                    else:
                        txt_pl_prev = "Rs. {:.2f} :red[(Rs. {:.2f})]"
                    st.write(txt_pl_prev.format(previous_close, prevdiff_value))
                    if todaypl_value > 0.0:
                        txt_pl_today = "P/L: :green[Rs. {:.2f} ({:.2f}%)]"
                    else:
                        txt_pl_today = "P/L: :red[Rs. {:.2f} ({:.2f}%)]"
                    st.write(txt_pl_today.format(todaypl_value, prevdiff_percent))
                st.divider()
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
        with stock_values_container.container(border=True, height=600):
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
                try:
                    previous_close = yfinance.Ticker(ticker=row).info['previousClose']
                except:
                    previous_close = current_price
                portfolio_data['equity'][row]["current price"] = current_price
                portfolio_data['equity'][row]["previous close"] = previous_close
                with open("data/portfolio.json", "w") as file:
                    json.dump(portfolio_data, file, indent=4)
                diff_value = current_price - previous_close
                diff_percent = diff_value/ previous_close * 100.00
                current_value = n_stocks * current_price
                pl_price = current_price - invested_price
                pl_value = current_value - invested_value # profit or loss value
                pl_percent = pl_value/invested_value*100.00
                st.session_state['total_invested_value_equity'] += invested_value # total invested value
                st.session_state['total_current_value_equity'] += current_value # total current value
                # display values
                equity_values = st.columns(len(st.session_state['equity_column_headers']))
                with equity_values[0]:
                    st.write(stock_name)
                with equity_values[1]:
                    st.write(f"{n_stocks}")
                with equity_values[2]:
                    st.write(f"Rs. {invested_price}/ share")
                    txt = "Rs. {:.2f}"
                    st.write(txt.format(invested_value))
                with equity_values[3]:
                    st.write(f"Rs. {current_price}/ share")
                    txt = "Rs. {:.2f}"
                    st.write(txt.format(current_value))
                with equity_values[4]:
                    if pl_price > 0.0:
                        txt_pl_price = ":green[Rs. {:.2f}/ share]"
                        txt_pl_value = ":green[Rs. {:.2f} ({:.2f}%)]"
                    else:
                        txt_pl_price = ":red[Rs. {:.2f}/ share]"
                        txt_pl_value = ":red[Rs. {:.2f} ({:.2f}%)]"
                    st.write(txt_pl_price.format(pl_price))
                    st.write(txt_pl_value.format(pl_value, pl_percent))
                with equity_values[5]:
                    st.write(f"Rs. {previous_close}/ share")
                    diff_value = current_price - previous_close
                    diff_percent = diff_value/ previous_close
                    if diff_value > 0.0:
                        txt_pl_prev = ":green[Rs. {:.2f} ({:.2f}%)]"
                    else:
                        txt_pl_prev = ":red[Rs. {:.2f} ({:.2f}%)]"
                    st.write(txt_pl_prev.format(diff_value, diff_percent))
                st.divider()
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

@st.dialog('Adding stock...')
def add_stock():
    # read portfolio file
    with open("data/portfolio.json", "r") as file:
        portfolio_data = json.load(file)
    new_dict = {}
    with st.container(border=True):

        add_stock_cols = st.columns(2)
        with add_stock_cols[0]:
            st.write("Enter stock name: ")
        with add_stock_cols[1]:
            stock_name = st.text_input("Stock name:", label_visibility="collapsed")

        add_stock_cols = st.columns(2)
        with add_stock_cols[0]:
            st.write("No. of shares bought: ")
        with add_stock_cols[1]:
            new_dict["no. of shares"] = st.number_input(label='n_stocks', label_visibility='collapsed', step=1)

        add_stock_cols = st.columns(2)
        with add_stock_cols[0]:
            st.write("Invested price: ")
        with add_stock_cols[1]:
            new_dict["invested price"] = st.number_input(label='n_stocks', label_visibility='collapsed', format="%.2f")

        if st.button("Add stock!"):
            portfolio_data['equity'][stock_name] = new_dict
            try:
                portfolio_data['equity'][stock_name]["current price"] = yfinance.Ticker(ticker=stock_name).info['currentPrice']
            except:
                portfolio_data['equity'][stock_name]["current price"] = portfolio_data['equity'][stock_name]["invested price"]
            try:
                portfolio_data['equity'][stock_name]["previous close"] = yfinance.Ticker(ticker=stock_name).info['previousClose']
            except:
                portfolio_data['equity'][stock_name]["previous close"] = portfolio_data['equity'][stock_name]["invested price"]

            stocks_name_list = list(portfolio_data["equity"].keys())
            stocks_name_list.sort()
            sorted_equities_dict = {stock: portfolio_data['equity'][stock] for stock in stocks_name_list}
            portfolio_data['equity'] = sorted_equities_dict
            with open("data/portfolio.json", "w") as file:
                json.dump(portfolio_data, file, indent=4)
            st.rerun()

@st.dialog('Editing details...')
def edit_details():
    # read portfolio file
    with open("data/portfolio.json", "r") as file:
        portfolio_data = json.load(file)
    stocks_name_list = list(portfolio_data["equity"].keys())
    with st.container(border=True):
        edit_details_cols = st.columns(2)
        with edit_details_cols[0]:
            st.write("Stock name: ")
        with edit_details_cols[1]:
            stock_selected = st.selectbox("Stock name:", stocks_name_list, label_visibility="collapsed")

        edit_details_cols = st.columns(2)
        with edit_details_cols[0]:
            st.write("No. of shares: ")
        with edit_details_cols[1]:
            new_quantity = st.number_input(value=portfolio_data['equity'][stock_selected]["no. of shares"], 
                                        label='n_stocks', label_visibility='collapsed')
            
        edit_details_cols = st.columns(2)
        with edit_details_cols[0]:
            st.write("Invested price: ")
        with edit_details_cols[1]:
            new_current_price = st.number_input(value=portfolio_data['equity'][stock_selected]["invested price"], 
                                                label='n_stocks', label_visibility='collapsed')
            
        if st.button("Save changes!"):
            portfolio_data['equity'][stock_selected]["no. of shares"] = new_quantity
            portfolio_data['equity'][stock_selected]["invested price"] = new_current_price
            with open("data/portfolio.json", "w") as file:
                json.dump(portfolio_data, file, indent=4)
            st.rerun()
    return

@st.dialog('Removing stock...')
def remove_stock():
    # read portfolio file
    with open("data/portfolio.json", "r") as file:
        portfolio_data = json.load(file)
    stocks_name_list = list(portfolio_data["equity"].keys())

    with st.container(border=True):
        remove_stock_cols = st.columns(2)
        with remove_stock_cols[0]:
            st.write("Stock name: ")
        with remove_stock_cols[1]:
            stock_selected = st.selectbox("Stock name:", stocks_name_list, label_visibility="collapsed")

        st.write(f"Do you want to remove **:red[{stock_selected}]**?")

        remove_stock_cols = st.columns(2)
        with remove_stock_cols[0]:    
            if st.button("Yes! Remove selected."):
                del portfolio_data['equity'][stock_selected]
                with open("data/portfolio.json", "w") as file:
                    json.dump(portfolio_data, file, indent=4)
                st.rerun()
        with remove_stock_cols[1]:
            if st.button("No! Close dialog."):
                st.rerun()
    return

########################################################################################################################

st.set_page_config(layout="wide")

st.title('Personal Finance - Equities')

controls_placeholder = st.empty()
column_header_container = st.empty()
stock_values_container = st.empty()
consolidated_container = st.empty()

initialize_session_state()

with controls_placeholder.container(border=True):
    controls_cols = st.columns([0.1,0.08,0.08,0.6])
    with controls_cols[0]:
        if st.button('Refresh values'):
            refresh_equity_values()
    with controls_cols[1]:
        if st.button('Add stock'):
            add_stock()
    with controls_cols[2]:
        if st.button('Edit details'):
            edit_details()
    with controls_cols[3]:
        if st.button('Remove stock'):
            remove_stock()
            
display_column_header()

load_equity_page()

display_consolidation()    

yfinance.Ticker(ticker='cipla.ns').info

# ticker = st.text_input(label='ticker', value='infy')
# stock_info = yfinance.Ticker(ticker=ticker).info

# st.text(stock_info['currentPrice'])

# for item in stock_info:
#     st.write(f'{item}: {stock_info[item]}')