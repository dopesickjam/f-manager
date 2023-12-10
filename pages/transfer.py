import streamlit as st
import pandas as pd
from datetime import datetime
import sys, logging, sqlite3
from shared.db import create_sqlite_connection, fetch_data, commit_data, get_category_list
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# To DO:
# add opportunity to transfer from UAH to USD

def main():
    #
    data = fetch_data("SELECT name FROM accounts")
    accounts_list_raw = pd.DataFrame(data).values.tolist()
    accounts_list = []
    for account in accounts_list_raw:
        account = account[0]
        accounts_list.append(account)
    #
    form_key = "transfer_form"
    with st.form(key=form_key, clear_on_submit=True):
        from_account            = st.selectbox("From", accounts_list)
        to_account              = st.selectbox("To", accounts_list)
        transfer_amount         = st.number_input("Transfer Amount")
        operation_date          = st.date_input("Date", value="today", format="YYYY-MM-DD")
        transaction_description = st.text_input("Comment")
        submitted               = st.form_submit_button("Submit")
    #
    if submitted:
        logging.info(submitted)

        data = fetch_data(f"SELECT balance FROM accounts WHERE name='{from_account}'")
        current_from_balance = pd.DataFrame(data).values.tolist()[0][0]

        data = fetch_data(f"SELECT balance FROM accounts WHERE name='{to_account}'")
        current_to_balance = pd.DataFrame(data).values.tolist()[0][0]

        new_from_balance = current_from_balance - transfer_amount
        new_to_balance   = current_to_balance + transfer_amount

        commit_data(f"UPDATE accounts SET balance={new_from_balance} WHERE name='{from_account}'")
        commit_data(f"UPDATE accounts SET balance={new_to_balance} WHERE name='{to_account}'")

        sql_query = (
            f"INSERT INTO transactions (transaction_type, global_name,"
            f"account, amount, currency, transaction_date, transaction_description)"
            f"VALUES ('Transfer', 'Transfer', '{from_account}',"
            f"'{transfer_amount}', 'UAH', '{operation_date}',"
            f"'{transaction_description}')"
        )
        commit_data(sql_query)

        st.success(f"Transfer added")

if __name__ == "__main__":
    main()