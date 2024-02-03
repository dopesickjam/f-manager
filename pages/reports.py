import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from shared.db import create_sqlite_connection, fetch_data
from datetime import datetime, timedelta

def main():
    data = ''
    c1, c2 = st.columns(2)
    with c1:
        statistic_expense = st.toggle('Expense statistic by category')
    with c2:
        statistic_income  = st.toggle('Income statistic by category')

    on = st.toggle('More filters:')
    if on:
        col1, col2 = st.columns(2)
        with col1:
            month = datetime.today() - timedelta(days=30)
            from_date = st.date_input("FROM:", value=month, format="YYYY-MM-DD")
        with col2:
            to_date = st.date_input("TO:", value="today", format="YYYY-MM-DD")

    statistic_type = ''
    if statistic_expense:
        data = fetch_data(f"SELECT category_name FROM categories WHERE category_type='Expense'")
        statistic_type = 'Expense'
    if statistic_income:
        data = fetch_data(f"SELECT category_name FROM categories WHERE category_type='Income'")
        statistic_type = 'Income'
    statistic_uah = {}
    statistic_usd = {}
    for element in data:
        if on:
            data = fetch_data(f"SELECT amount, currency FROM transactions WHERE category='{element[0]}' AND transaction_type='{statistic_type}' AND transaction_date BETWEEN '{from_date}' AND '{to_date}'")
        else:
            data = fetch_data(f"SELECT amount, currency FROM transactions WHERE category='{element[0]}' AND transaction_type='{statistic_type}'")
        summ_uah = 0
        summ_usd = 0
        for amount in data:
            if amount[1] == 'UAH':
                summ_uah = summ_uah + float(amount[0])
            elif amount[1] == 'USD':
                summ_usd = summ_usd + float(amount[0])
        if summ_uah:
            statistic_uah[element[0]] = summ_uah
        if summ_usd:
            statistic_usd[element[0]] = summ_usd

    if statistic_expense or statistic_income:
        st.dataframe(statistic_uah, hide_index=False, use_container_width=True)
        st.dataframe(statistic_usd, hide_index=False, use_container_width=True)

    go_to_main = st.button("go to main")
    if go_to_main:
        switch_page("main")

if __name__ == "__main__":
    main()