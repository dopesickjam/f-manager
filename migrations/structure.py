import sys, logging, os, sqlite3

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
DB_FILE = "db/local.db"

def create_database():
    """Create an SQLite database file."""
    if not os.path.exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as connection:
            pass

def create_table_accounts():
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                name TEXT PRIMARY KEY,
                balance REAL,
                currency TEXT
            )
        """)
        connection.commit()

def create_table_categories():
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                categories_id INTEGER PRIMARY KEY AUTOINCREMENT,
                root_category INTEGER,
                parent_category TEXT,
                category_name TEXT,
                category_type TEXT
            )
        """)
        connection.commit()

def create_table_transactions():
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT,
                global_name TEXT,
                account TEXT,
                category TEXT,
                amount TEXT,
                currency TEXT,
                transaction_date TEXT,
                transaction_description TEXT
            )
        """)
        connection.commit()

def create_table_exchange():
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange (
                name TEXT PRIMARY KEY,
                rate REAL,
                exchange_date TEXT
            )
        """)
        connection.commit()

def create_table_debt():
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS debt (
                debt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                debt_name TEXT,
                type TEXT,
                amount TEXT,
                currency TEXT,
                transaction_description TEXT
            )
        """)
        connection.commit()

def main():
    create_database()
    logging.info(f"Created database file: {DB_FILE}")

    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        create_table_accounts()
        create_table_categories()
        create_table_transactions()
        create_table_exchange()
        create_table_debt()
        logging.info("Migration 1: Init DB structure for the project.")

    logging.info("Migrations completed.")

if __name__ == "__main__":
    main()
