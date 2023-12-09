import streamlit as st
import pandas as pd
from datetime import datetime
import sys, logging, sqlite3
from shared.db import create_sqlite_connection, fetch_data

# CREATE TABLE transactions (
#     transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, 
#     transaction_type TEXT, 
#     global_name TEXT, 
#     account TEXT, 
#     category TEXT, 
#     amount TEXT, 
#     currency TEXT, 
#     transaction_date TEXT, 
#     transaction_description TEXT
# );

def main():
    data = fetch_data("SELECT transaction_type, account, category, amount, currency, transaction_date, transaction_description FROM transactions")

    #
    columns = ["Type", "Account", "Category", "Amount", "Currency", "Date", "Comment"]
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df)

if __name__ == "__main__":
    main()