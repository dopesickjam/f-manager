import streamlit as st
import pandas as pd
from datetime import datetime
import sys, logging, sqlite3
from shared.db import create_sqlite_connection, fetch_data, commit_data, get_category_list

def main():
    #
    data = fetch_data("SELECT name FROM accounts")
    accounts_list_raw = pd.DataFrame(data).values.tolist()
    accounts_list = []
    for account in accounts_list_raw:
        account = account[0]
        accounts_list.append(account)
    #
    form_key = "transaction_form"
    with st.form(key=form_key, clear_on_submit=True):
        transaction_list = ["Income"]
        transaction_type = st.selectbox("Type", transaction_list)
        account = st.selectbox("Account", accounts_list) 
        category = st.selectbox("Category", get_category_list("Income")) 
        amount = st.number_input("Amount")
        transaction_description = st.text_input("Comment")
        submitted = st.form_submit_button("Submit")
    #
    if submitted:
        logging.info(submitted)

        #
        data = fetch_data(f"SELECT balance FROM accounts WHERE name='{account}'")
        current_balance = pd.DataFrame(data).values.tolist()[0][0]
        new_balance = current_balance + amount
        
        commit_data(f"UPDATE accounts SET balance={new_balance} WHERE name='{account}'")
        #
        data = fetch_data(f"SELECT currency FROM accounts WHERE name='{account}'")
        currency = pd.DataFrame(data).values.tolist()[0][0]

        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%d-%m-%Y")
        sql_query = (
            f"INSERT INTO transactions (transaction_type, global_name,"
            f"account, category, amount, currency, transaction_date, transaction_description)"
            f"VALUES ('{transaction_type}', '{transaction_type}', '{account}',"
            f"'{category}', '{amount}', '{currency}', '{formatted_date}',"
            f"'{transaction_description}')"
        )
        commit_data(sql_query)

        st.success(f"Transaction '{transaction_type}' added")
        st.code(sql_query, language="sql")

if __name__ == "__main__":
    main()