import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
from datetime import datetime
import sys, logging, requests
from shared.db import create_sqlite_connection, fetch_data, commit_data
from shared.api import get_exchange_rate
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def sum_of_all_transaction(transaction_type):
    data = fetch_data(f"SELECT amount, currency FROM transactions WHERE transaction_type='{transaction_type}'")
    uah = 0
    usd = 0
    for element in data:
        if element[1] == 'UAH':
            uah = uah + float(element[0])
        elif element[1] == 'USD':
            usd = usd + float(element[0])
    return "{:.2f}".format(uah), "{:.2f}".format(usd)

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
        pass
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

    df = pd.DataFrame(
        {
            "sum by currency": [f'{"{:.2f}".format(summ_uah)} UAH', f'{"{:.2f}".format(sum_usd)} USD'],
            "all sum in currency": [f'{"{:.2f}".format(summ_uah + sum_usd * uah_to_usd)} UAH', f'{"{:.2f}".format(sum_usd + summ_uah / uah_to_usd)} USD'],
        }
    )
    st.dataframe(df, hide_index=True, use_container_width=True)

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
    go_to_reports      = st.button("reports")
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
    if go_to_reports:
        switch_page("reports")

    uah_expense, usd_expense = sum_of_all_transaction('Expense')
    uah_income, usd_income   = sum_of_all_transaction('Income')

    df = pd.DataFrame(
        {
            "all expense": [f'{uah_expense} UAH', f'{usd_expense} USD'],
            "all income": [f'{uah_income} UAH', f'{usd_income} USD'],
        }
    )
    st.dataframe(df, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    main()