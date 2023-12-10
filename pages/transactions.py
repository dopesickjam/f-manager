import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys, logging, sqlite3
from shared.db import create_sqlite_connection, fetch_data
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# TO DO
# add filter by date FROM TO
# to sum all incomes and expenses transaction by filter
# add statistic by category
# add opportunity to delete a transaction
def main():
    option = st.selectbox(
    'Chose transaction list',
    ('ALL', 'Expense', 'Income', 'Transfer'))
    to_date = datetime.today()
    from_date   = datetime.today() - timedelta(days=365)
    on = st.toggle('More filters:')
    if on:
        col1, col2 = st.columns(2)
        with col1:
            month = datetime.today() - timedelta(days=30)
            from_date = st.date_input("FROM:", value=month, format="YYYY-MM-DD")
        with col2:
            to_date = st.date_input("TO:", value="today", format="YYYY-MM-DD")

    if option == 'ALL':
        data = fetch_data(f"SELECT transaction_type, account, category, amount, currency, transaction_date, transaction_description FROM transactions WHERE transaction_date BETWEEN '{from_date}' AND '{to_date}'")
    else:
        data = fetch_data(f"SELECT transaction_type, account, category, amount, currency, transaction_date, transaction_description FROM transactions WHERE transaction_type='{option}' AND transaction_date BETWEEN '{from_date}' AND '{to_date}'")
    #
    columns = ["Type", "Account", "Category", "Amount", "Currency", "Date", "Comment"]
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df)

if __name__ == "__main__":
    main()