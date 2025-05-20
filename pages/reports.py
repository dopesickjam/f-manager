import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from shared.db import create_sqlite_connection, fetch_data
from datetime import datetime, timedelta
import pandas as pd

def uCategory(global_name):
  return fetch_data(f"SELECT DISTINCT category FROM transactions WHERE global_name = '{global_name}';")

def uSumm(category, global_name, tYear, tMonth):
  summ_uah = 0
  summ_usd = 0
  data = fetch_data(f"SELECT category, amount, currency, transaction_date FROM transactions WHERE category = '{category}' AND global_name = '{global_name}' AND transaction_date LIKE '{tYear}-{tMonth}%';")
  for i in data:
    if i[2] == 'UAH':
      summ_uah = summ_uah + float(i[1])
    elif i[2] == 'USD':
      summ_usd = summ_usd + float(i[1])

  return summ_uah, summ_usd

def main():
    data = ''
    c1, c2 = st.columns(2)
    with c1:
        statistic_expense = st.toggle('Expense statistic by category')
    with c2:
        statistic_income  = st.toggle('Income statistic by category')

    from_to = st.toggle('FromTo statistic:')
    monthly = st.toggle('Monthly statistic:')
    if from_to:
        col1, col2 = st.columns(2)
        with col1:
            month = datetime.today().replace(day=1)
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
        if from_to:
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

    if monthly:
      option = st.selectbox(
        "YEAR",
        ("2021", "2022", "2023", "2024", "2025"),
      )

      statistic_frame_uah = []
      statistic_frame_usd = []

      uniq_category = uCategory('Expense')
      for element in uniq_category:
        statistic_uah = {}
        statistic_usd = {}
        statistic_uah['category'] = element[0]
        for i in range(1,13):
          i = f"{i:02d}"
          summ_uah, summ_usd = uSumm(element[0], 'Expense', option, i)
          statistic_uah[i]  = summ_uah
        statistic_frame_uah.append(statistic_uah)

      df = pd.DataFrame(statistic_frame_uah)

      st.dataframe(df, use_container_width=True)

    go_to_main = st.button("go to main")
    if go_to_main:
        switch_page("main")

if __name__ == "__main__":
    main()