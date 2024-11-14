import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, \
    QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import sqlite3


class FinanceManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.setWindowTitle("Finance Manager")
        self.setGeometry(100, 100, 400, 300)

        # Main layout
        layout = QVBoxLayout()

        # Form layout for transaction details
        form_layout = QFormLayout()

        self.date_input = QLineEdit(self)
        self.amount_input = QLineEdit(self)
        self.type_input = QLineEdit(self)
        self.category_input = QLineEdit(self)
        self.description_input = QLineEdit(self)

        form_layout.addRow("Date (YYYY-MM-DD):", self.date_input)
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Type (Income/Expense):", self.type_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Description (optional):", self.description_input)

        layout.addLayout(form_layout)

        # Add transaction button
        add_button = QPushButton("Add Transaction", self)
        add_button.clicked.connect(self.add_transaction)
        layout.addWidget(add_button)

        # Add View Transactions button
        view_button = QPushButton("View Transactions", self)
        view_button.clicked.connect(self.open_view_transactions_window)
        layout.addWidget(view_button)

        self.setLayout(layout)

    def add_transaction(self):
        # Retrieve data from input fields
        date = self.date_input.text()
        amount = float(self.amount_input.text())
        transaction_type = self.type_input.text()
        category = self.category_input.text()
        description = self.description_input.text() if self.description_input.text() else None

        # Insert into the database
        conn = sqlite3.connect('data/finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO transactions (date, amount, type, category, description)
        VALUES (?, ?, ?, ?, ?)
        ''', (date, amount, transaction_type, category, description))

        conn.commit()
        conn.close()

        # Clear the input fields
        self.date_input.clear()
        self.amount_input.clear()
        self.type_input.clear()
        self.category_input.clear()
        self.description_input.clear()

        # Show a confirmation message
        confirmation_label = QLabel("Transaction added successfully!")
        self.layout().addWidget(confirmation_label)

    def open_view_transactions_window(self):
        self.view_window = ViewTransactionsWindow()
        self.view_window.show()


class ViewTransactionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Transactions")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Create a table to display transactions
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Fetch data from the database
        self.fetch_data()

        self.setLayout(layout)

    def fetch_data(self):
        conn = sqlite3.connect('data/finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions')
        transactions = cursor.fetchall()

        self.table.setRowCount(len(transactions))  # Set the number of rows
        self.table.setColumnCount(
            6)  # Set the number of columns (ID, Date, Amount, Type, Category, Description)

        for row_num, transaction in enumerate(transactions):
            for col_num, value in enumerate(transaction):
                self.table.setItem(row_num, col_num,
                                   QTableWidgetItem(str(value)))

        conn.close()

if __name__ == "__main__":
    # Create the application and main window
    app = QApplication(sys.argv)
    window = FinanceManagerApp()
    window.show()
    sys.exit(app.exec())