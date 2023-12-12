import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys, logging, sqlite3
from streamlit_extras.switch_page_button import switch_page
from shared.db import create_sqlite_connection, fetch_data
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# TO DO
# add statistic by category
# add opportunity to delete a transaction
def main():
    tl1, tl2 = st.columns(2)
    with tl1:
        st.title(f'Statistic')
    with tl2:
        go_to_main = st.button("main")
        if go_to_main:
            switch_page("main")
    option = st.selectbox(
    'Chose transaction list',
    ('ALL', 'Expense', 'Income', 'Transfer'))
    on = st.toggle('More filters:')
    if on:
        col1, col2 = st.columns(2)
        with col1:
            month = datetime.today() - timedelta(days=30)
            from_date = st.date_input("FROM:", value=month, format="YYYY-MM-DD")
        with col2:
            to_date = st.date_input("TO:", value="today", format="YYYY-MM-DD")

    if on:
        if option == 'ALL':
            data = fetch_data(f"SELECT transaction_type, account, category, amount, currency, transaction_date, transaction_description FROM transactions WHERE transaction_date BETWEEN '{from_date}' AND '{to_date}'")
        else:
            data = fetch_data(f"SELECT transaction_type, account, category, amount, currency, transaction_date, transaction_description FROM transactions WHERE transaction_type='{option}' AND transaction_date BETWEEN '{from_date}' AND '{to_date}'")
    else:
        if option == 'ALL':
            data = fetch_data(f"SELECT transaction_type, account, category, amount, currency, transaction_date, transaction_description FROM transactions")
        else:
            data = fetch_data(f"SELECT transaction_type, account, category, amount, currency, transaction_date, transaction_description FROM transactions WHERE transaction_type='{option}'")

    #
    columns = ["Type", "Account", "Category", "Amount", "Currency", "Date", "Comment"]
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df, hide_index=True)
    summ = 0
    if option == 'Expense' or option == 'Income':
        for transaction in data:
            summ = summ + float(transaction[3])
        st.text(f'Summ of {option}s: {summ}')

if __name__ == "__main__":
    main()