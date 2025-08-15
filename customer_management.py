# customer_management.py
from datetime import datetime
from database import get_connection

class CustomerManager:
    def create_account(self, name: str, initial_balance: float = 0.0):
        """Create a new account and return the customer ID."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO customers(name, balance) VALUES(?, ?)",
                    (name, initial_balance))
        customer_id = cur.lastrowid

        # Record as deposit if initial balance > 0
        if initial_balance > 0:
            cur.execute(
                "INSERT INTO transactions(customer_id, type, amount, balance_after, timestamp) VALUES (?, ?, ?, ?, ?)",
                (customer_id, "Deposit", initial_balance, initial_balance, datetime.now().isoformat())
            )

        conn.commit()
        conn.close()
        return customer_id

    def get_balance(self, customer_id: int):
        """Get the balance for a given customer ID."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM customers WHERE id=?", (customer_id,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None
