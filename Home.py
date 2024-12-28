import streamlit as st
import json

################################## FUNCTION DEFINITIONS ################################################################

# initialize session state
def initialize_session_state():
    # initialize total equity investment and current value
    if 'total_current_value_equity' not in st.session_state:
        st.session_state['total_current_value_equity'] = 0.0
    if 'total_invested_value_equity' not in st.session_state:
        st.session_state['total_invested_value_equity'] = 0.0

def load_equity():
    with open("data/portfolio.json", "r") as file:
        portfolio_data = json.load(file)
    st.session_state['total_current_value_equity'] = 0.0
    st.session_state['total_invested_value_equity'] = 0.0
    try:
        for row in portfolio_data["equity"]:
            n_stocks = portfolio_data['equity'][row]["no. of shares"]
            current_price = portfolio_data['equity'][row]["current price"]
            current_value = n_stocks * current_price
            invested_price = portfolio_data['equity'][row]["invested price"]
            invested_value = n_stocks * invested_price
            st.session_state['total_current_value_equity'] += current_value
            st.session_state['total_invested_value_equity'] += invested_value

        with equity_container.container(border=True):
            st.write("**EQUITIES**")
            st.write(f'Total invested value: {st.session_state["total_invested_value_equity"]}')
            st.write(f'Total current value: {st.session_state["total_current_value_equity"]}')
            txt = "Total profit/ loss value: {:.2f}"
            st.write(txt.format((st.session_state["total_current_value_equity"]-st.session_state["total_invested_value_equity"])))
            txt = "Total profit/ loss percentage: {:.2f}"
            st.write(txt.format((st.session_state["total_current_value_equity"]-st.session_state["total_invested_value_equity"])/st.session_state["total_invested_value_equity"]*100.0))

    except Exception as e:
        st.error(str(e))

########################################################################################################################

st.set_page_config(layout="wide")

st.title('Personal Finance - Dashboard')

initialize_session_state()

equity_container = st.empty()

load_equity()


