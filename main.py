import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
from datetime import datetime
import sys, logging, requests
from shared.db import create_sqlite_connection, fetch_data, commit_data
from shared.api import get_exchange_rate
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# TO do:
# more statistic (by day, last month, current month, etc)

def main():
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    data = fetch_data('SELECT exchange_date FROM exchange')
    if not data:
        logging.info('Table is empty, get a new record')
        uah_to_usd = get_exchange_rate()
        commit_data(f"INSERT INTO exchange (name, rate, exchange_date) VALUES ('uah_to_usd', '{uah_to_usd}', '{formatted_date}')")
    elif data[0][0] < formatted_date:
        logging.info('The record is old, get a new record')
        uah_to_usd = get_exchange_rate()
        commit_data(f"UPDATE exchange SET rate='{uah_to_usd}', exchange_date='{formatted_date}' WHERE name='uah_to_usd'")
    else:
        logging.info('The record is exactly')
        data = fetch_data('SELECT rate FROM exchange')
        uah_to_usd = data[0][0]

    data = fetch_data('SELECT balance, currency FROM accounts')
    summ_uah = 0
    sum_usd = 0
    for balance in data:
        if balance[1] == 'UAH':
            summ_uah = balance[0] + summ_uah
        elif balance[1] == 'USD':
            sum_usd = balance[0] + sum_usd

    s1, s2 = st.columns(2)
    with s1:
        st.text(f'{summ_uah} UAH')
        st.text(f'{sum_usd} UAH')
    with s2:
        st.text(f'{summ_uah + sum_usd * uah_to_usd} all in UAH')
        st.text(f'{sum_usd + summ_uah / uah_to_usd} all in USD')

    st.markdown(
    """
    <style>
    button {
        padding: 10px 20px;
        min-width: 100%;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    go_to_accounts     = st.button("accounts")
    go_to_incomes      = st.button("incomes")
    go_to_expenses     = st.button("expenses")
    go_to_transfer     = st.button("transfer")
    go_to_transactions = st.button("transactions")
    if go_to_accounts:
        switch_page("accounts")
    if go_to_incomes:
        switch_page("incomes")
    if go_to_expenses:
        switch_page("expenses")
    if go_to_transfer:
        switch_page("transfer")
    if go_to_transactions:
        switch_page("transactions")

if __name__ == "__main__":
    main()