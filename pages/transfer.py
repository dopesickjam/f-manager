import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
import sys, logging, sqlite3
from shared.db import create_sqlite_connection, fetch_data, commit_data, get_category_list
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def get_currency(wallet):
    data = fetch_data(f"SELECT currency FROM accounts WHERE name='{wallet}'")
    if data:
        return data[0][0]

def main():
    tl1, tl2 = st.columns(2)
    with tl1:
        st.title(f'Transfer')
    with tl2:
        go_to_main = st.button("main")
        if go_to_main:
            switch_page("main")
    #
    data = fetch_data("SELECT name FROM accounts")
    accounts_list_raw = pd.DataFrame(data).values.tolist()
    accounts_list = []
    for account in accounts_list_raw:
        account = account[0]
        accounts_list.append(account)

    col1, col2 = st.columns(2)
    with col1:
        from_account  = st.selectbox("From wallet", accounts_list, index=None)
        currency_from = get_currency(from_account)
    with col2:
        to_account   = st.selectbox("To wallet", accounts_list, index=None)
        currency_to  = get_currency(to_account)

    submitted = False
    form_key = "transfer_form"
    if currency_from == None and currency_to == None or currency_from == None or currency_to == None:
        pass
    elif currency_from == currency_to:
        with st.form(key=form_key, clear_on_submit=True):
            transfer_amount         = st.number_input("Transfer Amount", disabled=False)
            operation_date          = st.date_input("Date", value="today", format="YYYY-MM-DD")
            submitted               = st.form_submit_button("Submit")
    elif currency_from != currency_to:
        with st.form(key=form_key, clear_on_submit=True):
            transfer_from           = st.number_input("Transfer From", disabled=False)
            transfer_to             = st.number_input("Transfer To", disabled=False)
            operation_date          = st.date_input("Date", value="today", format="YYYY-MM-DD")
            submitted               = st.form_submit_button("Submit")
            if currency_from != currency_to:
                transfer_rate = 0
                if transfer_from > transfer_to:
                    transfer_rate = transfer_from / transfer_to
                elif transfer_from < transfer_to:
                    transfer_rate = transfer_to / transfer_from
            st.write(f'Transfer rate: {transfer_rate}')

    if submitted:
        logging.info(submitted)

        data = fetch_data(f"SELECT balance FROM accounts WHERE name='{from_account}'")
        current_from_balance = pd.DataFrame(data).values.tolist()[0][0]

        data = fetch_data(f"SELECT balance FROM accounts WHERE name='{to_account}'")
        current_to_balance = pd.DataFrame(data).values.tolist()[0][0]

        if currency_from == currency_to:
            new_from_balance = current_from_balance - transfer_amount
            new_to_balance   = current_to_balance + transfer_amount
            #
            transaction_description = f'+{transfer_amount} {to_account}'
        elif currency_from != currency_to:
            new_from_balance = current_from_balance - transfer_from
            new_to_balance   = current_to_balance + transfer_to
            # for transaction
            transfer_amount         = f'-{transfer_from}'
            transaction_description = f'+{transfer_to} {to_account}'

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