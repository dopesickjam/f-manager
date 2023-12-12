import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import sys, logging
from shared.db import create_sqlite_connection, fetch_data
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# TO do:
# ADD summ by account, by accounts in UAH and USD
# more statistic (by day, last month, current month, etc)

# add page for currency setting, like category
def main():
    data = fetch_data('SELECT balance FROM accounts')
    summ = 0
    for balance in data:
        summ = balance[0] + summ

    st.title(f'{summ} UAH')

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

    go_to_accounts = st.button("accounts")
    go_to_incomes  = st.button("incomes")
    go_to_expenses = st.button("expenses")
    go_to_transfer = st.button("transfer")
    if go_to_accounts:
        switch_page("accounts")
    if go_to_incomes:
        switch_page("incomes")
    if go_to_expenses:
        switch_page("expenses")
    if go_to_transfer:
        switch_page("transfer")

if __name__ == "__main__":
    main()