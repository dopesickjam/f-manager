import streamlit as st
import pandas as pd
import sys, logging, sqlite3, numpy
from shared.db import create_sqlite_connection, fetch_data, commit_data, get_wallets
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def main():
    st.title(f'Debt')
    #
    data = fetch_data('SELECT debt_id, debt_name, type, amount, currency, transaction_description FROM debt')
    columns = ["ID", "Name", "Type", "Amount", "Currency", "Comment"]
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df, hide_index=True, use_container_width=True)
    form_key = "debt_form"
    with st.form(key=form_key, clear_on_submit=True):
        whom                    = st.text_input("Whom")
        account                 = st.selectbox("Account", get_wallets(), index=None)
        type                    = st.selectbox("Type", ["Lend", "Borrow"], index=None)
        amount                  = st.number_input("Amount")
        operation_date          = st.date_input("Date", value="today", format="YYYY-MM-DD")
        transaction_description = st.text_input("Comment")
        submitted               = st.form_submit_button("Submit")
    #
    if submitted:
        data = fetch_data(f"SELECT currency, balance FROM accounts WHERE name='{account}'")
        currency = data[0][0]
        balance = data[0][1]

        data = fetch_data(f'SELECT debt_name FROM debt WHERE type="{type}" AND currency="{currency}"')
        exist = False
        for debt_check in data:
            if debt_check[0] == whom:
                exist = True
                break

        if type == 'Lend':
            new_amount_account = float(balance) - amount
        elif type == 'Borrow':
            new_amount_account = float(balance) + amount
        commit_data(f"UPDATE accounts SET balance={new_amount_account} WHERE name='{account}'")

        if exist:
            data = fetch_data(f'SELECT amount FROM debt WHERE debt_name="{whom}" AND type="{type}" AND currency="{currency}"')
            current_amount = data[0][0]
            new_amount_debt = float(current_amount) + amount
            sql_query = (
                f"UPDATE debt SET amount={new_amount_debt} WHERE debt_name='{whom}' AND type='{type}' AND currency='{currency}'"
            )
        else:
            sql_query = (
                f"INSERT INTO debt (debt_name, type, amount, currency, transaction_description)"
                f"VALUES ('{whom}', '{type}', '{amount}', '{currency}', '{transaction_description}')"
            )
        commit_data(sql_query)

        sql_query = (
            f"INSERT INTO transactions (transaction_type, global_name,"
            f"account, category, amount, currency, transaction_date, transaction_description)"
            f"VALUES ('Debt', '{whom}', '{account}',"
            f"'{type}', '{amount}', '{currency}', '{operation_date}',"
            f"'{whom}')"
        )
        commit_data(sql_query)

        st.success(f"Transaction added")
        st.rerun()

    delete_debt = st.toggle('Delete Debt')
    if delete_debt:
        agree = st.checkbox("I agree")
        for index, row in df.iterrows():
            if st.button(f"Delete {row['ID']}", key=f"delete_{row['ID']}", disabled=numpy.logical_not(agree)):
                commit_data(f"DELETE FROM debt WHERE debt_id='{row['ID']}'")
                st.rerun()

if __name__ == "__main__":
    main()