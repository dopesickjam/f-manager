import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys, logging, sqlite3
from streamlit_extras.switch_page_button import switch_page
from shared.db import create_sqlite_connection, fetch_data, commit_data
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def main():
    st.title(f'Statistic')

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
    st.dataframe(df, hide_index=True, use_container_width=True)
    summ = 0
    if option == 'Expense' or option == 'Income':
        for transaction in data:
            summ = summ + float(transaction[3])
        st.text(f'Summ of {option}s: {summ}')

    transaction_on = st.toggle('Activate modify on transaction')
    if transaction_on:
        transaction_to = st.selectbox('Chose transaction', data, index=None)

        delete = st.toggle('Delete?')
        update = st.toggle('Update?')
        if delete:
            delete_button = st.button('Delete!')

            if delete_button:
                transaction_type = transaction_to[0]
                account          = transaction_to[1]
                category         = transaction_to[2]
                amount           = transaction_to[3]
                currency         = transaction_to[4]
                transaction_date = transaction_to[5]
                comment          = transaction_to[6]

                logging.info('Delete operations')
                if transaction_type == 'Transfer':
                    commit_data(f"DELETE FROM transactions WHERE transaction_type='{transaction_type}' AND account='{account}' AND category IS NULL AND amount='{amount}' AND currency='{currency}' AND transaction_date='{transaction_date}'")
                else:
                    commit_data(f"DELETE FROM transactions WHERE transaction_type='{transaction_type}' AND account='{account}' AND category='{category}' AND amount='{amount}' AND currency='{currency}' AND transaction_date='{transaction_date}'")
                logging.info('Transaction is deleted')

                data = fetch_data(f"SELECT balance FROM accounts WHERE name='{account}'")
                current_balance = pd.DataFrame(data).values.tolist()[0][0]
                logging.info(f'Current balance at {account}: {current_balance}')

                if transaction_type == 'Expense':
                    new_balance = current_balance + float(amount)
                elif transaction_type == 'Income':
                    new_balance = current_balance - float(amount)
                elif transaction_type == 'Transfer':
                    new_balance = current_balance + float(amount)
                    data = fetch_data(f"SELECT balance FROM accounts WHERE name='{comment.split(' ')[1]}'")
                    revert_balance = data[0][0] - float(comment.split(' ')[0][1:])
                    commit_data(f"UPDATE accounts SET balance={revert_balance} WHERE name='{comment.split(' ')[1]}'")
                    logging.info(f"Balance is revert at {comment.split(' ')[1]}, new balance: {revert_balance}")

                commit_data(f"UPDATE accounts SET balance={new_balance} WHERE name='{account}'")
                logging.info(f'Balance is updated at {account}, new balance: {new_balance}')
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