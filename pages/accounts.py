import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import sys, logging, numpy
from shared.db import create_sqlite_connection, fetch_data, commit_data
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def main():
    st.title("Wallets")

    col1, col2 = st.columns(2)
    #
    data = fetch_data('SELECT name, balance, currency FROM accounts')
    columns = ["Name", "Balance", "Currency"]
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df, hide_index=True, use_container_width=True)
    delete_on = st.toggle('Activate delete wallet')
    add_on    = st.toggle('Activate add wallet')
    if delete_on:
        agree = st.checkbox("I agree")
    #
    if delete_on:
        for index, row in df.iterrows():
            if st.button(f"Delete {row['Name']}", key=f"delete_{row['Name']}", disabled=numpy.logical_not(agree)):
                commit_data(f"DELETE FROM accounts WHERE name='{row['Name']}'")
                st.success(f"Deleted row for account '{row['Name']}'")
                st.rerun()

    #
    if add_on:
        form_key = "account_form"
        with st.form(key=form_key, clear_on_submit=True):
            name = st.text_input("Name")
            balance = st.number_input("Balance")
            currency_options = ["UAH", "USD", "EUR"]
            currency = st.selectbox("Currency", currency_options, index=None)
            submitted = st.form_submit_button("Submit")

        if submitted:
            logging.info(submitted)
            sql_query = f"INSERT INTO accounts (name, balance, currency) VALUES ('{name}', {balance}, '{currency}')"
            commit_data(sql_query)

            st.success(f"Account '{name}' added with balance {balance} {currency}")
            st.code(sql_query, language="sql")
            st.rerun()

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
    go_to_main = st.button("go to main")
    if go_to_main:
        switch_page("main")

if __name__ == "__main__":
    main()