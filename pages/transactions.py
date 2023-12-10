import streamlit as st
import pandas as pd
from datetime import datetime
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

    if option == 'ALL':
        data = fetch_data("SELECT transaction_type, account, category, amount, currency, transaction_date, transaction_description FROM transactions")
    else:
        data = fetch_data(f"SELECT transaction_type, account, category, amount, currency, transaction_date, transaction_description FROM transactions WHERE transaction_type='{option}'")
    #
    columns = ["Type", "Account", "Category", "Amount", "Currency", "Date", "Comment"]
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df)

if __name__ == "__main__":
    main()