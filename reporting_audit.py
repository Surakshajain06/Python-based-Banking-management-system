# reporting_audit.py
from database import get_connection

class ReportingAudit:
    def get_transactions(self, customer_id: int):
        """Return all transactions for a customer."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT type, amount, balance_after, timestamp FROM transactions WHERE customer_id=?", (customer_id,))
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_all_customers(self):
        """Return summary of all customers."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, balance FROM customers")
        rows = cur.fetchall()
        conn.close()
        return rows
