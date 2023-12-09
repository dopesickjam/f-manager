import streamlit as st
import pandas as pd
import sys, logging, sqlite3
from shared.db import create_sqlite_connection, fetch_data, commit_data

# CREATE TABLE categories (
#     categories_id INTEGER PRIMARY KEY AUTOINCREMENT, 
#     root_category INTEGER, 
#     parent_category TEXT,
#     category_name TEXT,
#     category_type TEXT
# );

def main():
    data = fetch_data("SELECT category_name, parent_category, root_category, category_type FROM categories")

    #
    columns = ["Name", "Parent", "Is root?", "Type"]
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df)

    #
    data = fetch_data(f"SELECT category_name FROM categories WHERE root_category='True'")
    parents_list_raw = pd.DataFrame(data).values.tolist()
    parents_list = ['']
    for category in parents_list_raw:
        category = category[0]
        parents_list.append(category)
    #
    form_key = "category_form"
    with st.form(key=form_key, clear_on_submit=True):
        category_list = ["", "Income", "Expense"]
        category_type = st.selectbox("Type", category_list)
        root_category   = st.checkbox("Set like a root category")
        category_name   = st.text_input("Category Name")
        parent_category = st.selectbox("Parent Category", parents_list) 
        submitted = st.form_submit_button("Submit")

    if submitted:
        logging.info(submitted)

        sql_query = (
            f"INSERT INTO categories (root_category, parent_category, category_name, category_type)"
            f"VALUES ('{root_category}', '{parent_category}', '{category_name}', '{category_type}')"
        )
        commit_data(sql_query)

        st.success(f"Category '{category_name}' added")
        st.code(sql_query, language="sql")
        st.rerun()

if __name__ == "__main__":
    main()