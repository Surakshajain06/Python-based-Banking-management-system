# transaction_handling.py
from datetime import datetime
from database import get_connection

class TransactionManager:
    def deposit(self, customer_id: int, amount: float):
        """Deposit money into account."""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT balance FROM customers WHERE id=?", (customer_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return "Customer not found."

        new_balance = row[0] + amount
        cur.execute("UPDATE customers SET balance=? WHERE id=?", (new_balance, customer_id))
        cur.execute(
            "INSERT INTO transactions(customer_id, type, amount, balance_after, timestamp) VALUES (?, ?, ?, ?, ?)",
            (customer_id, "Deposit", amount, new_balance, datetime.now().isoformat())
        )

        conn.commit()
        conn.close()
        return f"Deposited {amount}. New balance: {new_balance}"

    def withdraw(self, customer_id: int, amount: float):
        """Withdraw money from account."""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT balance FROM customers WHERE id=?", (customer_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return "Customer not found."

        if row[0] < amount:
            conn.close()
            return "Insufficient funds."

        new_balance = row[0] - amount
        cur.execute("UPDATE customers SET balance=? WHERE id=?", (new_balance, customer_id))
        cur.execute(
            "INSERT INTO transactions(customer_id, type, amount, balance_after, timestamp) VALUES (?, ?, ?, ?, ?)",
            (customer_id, "Withdrawal", amount, new_balance, datetime.now().isoformat())
        )

        conn.commit()
        conn.close()
        return f"Withdrew {amount}. New balance: {new_balance}"
