import sqlite3

def create_sqlite_connection():
    return sqlite3.connect("local.db")

def fetch_data(sql):
    connection = create_sqlite_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()
    return data

def commit_data(sql):
    connection = create_sqlite_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()

def get_category_list(category_type):
    root_category  = fetch_data(f"SELECT category_name FROM categories WHERE root_category='True' AND category_type='{category_type}' ORDER BY category_name")
    child_category = fetch_data(f"SELECT parent_category, category_name FROM categories WHERE root_category='False' AND category_type='{category_type}' ORDER BY parent_category")
    
    categories_list = []
    for parent in root_category:
        categories_list.append(parent[0])
        for child in child_category:
            if parent[0] == child[0]:
                categories_list.append(f"{parent[0]}/{child[1]}")
    return categories_list