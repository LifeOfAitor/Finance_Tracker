import sqlite3

# create database if it doesn't exist
def create_database():
    # Path to the database file
    db_path = 'data/finance_manager.db'

    # Connect to the database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the 'transactions' table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL CHECK (type IN ('Income', 'Expense')),
        category TEXT NOT NULL,
        description TEXT
    )
    ''')

    # Commit and close
    conn.commit()
    conn.close()

    print("Database and table created successfully.")

def add_transaction(date, amount, transaction_type, category, description=None):
    # Connect to the database
    conn = sqlite3.connect('data/finance_manager.db')
    cursor = conn.cursor()

    # Insert transaction into the database
    cursor.execute('''
    INSERT INTO transactions (date, amount, type, category, description)
    VALUES (?, ?, ?, ?, ?)
    ''', (date, amount, transaction_type, category, description))

    # Commit and close
    conn.commit()
    conn.close()

    print("Transaction added successfully.")

def view_transactions():
    # Connect to the database
    conn = sqlite3.connect('data/finance_manager.db')
    cursor = conn.cursor()

    # Fetch all transactions
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()

    # Display the transactions
    for transaction in transactions:
        print(transaction)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    create_database()
    add_transaction("13/11/24", 7, "Income", "Game", "Steam games")
    add_transaction('2024-11-14', 1500, 'Income', 'Salary','Monthly salary payment')