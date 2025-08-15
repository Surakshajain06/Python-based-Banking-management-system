# app_gui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from customer_management import CustomerManager
from transaction_handling import TransactionManager
from reporting_audit import ReportingAudit

cm = CustomerManager()
tm = TransactionManager()
ra = ReportingAudit()

root = tk.Tk()
root.title("Banking Management System")
root.geometry("400x400")

def create_account():
    name = simpledialog.askstring("Account", "Enter customer name:")
    balance = simpledialog.askfloat("Balance", "Enter initial balance:")
    if name is not None and balance is not None:
        cid = cm.create_account(name, balance)
        messagebox.showinfo("Success", f"Account created! Customer ID: {cid}")

def deposit():
    cid = simpledialog.askinteger("Deposit", "Enter customer ID:")
    amt = simpledialog.askfloat("Deposit", "Enter amount:")
    if cid and amt:
        messagebox.showinfo("Info", tm.deposit(cid, amt))

def withdraw():
    cid = simpledialog.askinteger("Withdraw", "Enter customer ID:")
    amt = simpledialog.askfloat("Withdraw", "Enter amount:")
    if cid and amt:
        messagebox.showinfo("Info", tm.withdraw(cid, amt))

def view_balance():
    cid = simpledialog.askinteger("Balance", "Enter customer ID:")
    if cid:
        bal = cm.get_balance(cid)
        if bal is not None:
            messagebox.showinfo("Balance", f"Balance: {bal}")
        else:
            messagebox.showerror("Error", "Customer not found.")

def view_transactions():
    cid = simpledialog.askinteger("Transactions", "Enter customer ID:")
    if cid:
        txns = ra.get_transactions(cid)
        if txns:
            msg = "\n".join([f"{t[0]}: {t[1]} | Balance: {t[2]} | {t[3]}" for t in txns])
            messagebox.showinfo("Transactions", msg)
        else:
            messagebox.showinfo("Transactions", "No transactions found.")

def all_customers():
    customers = ra.get_all_customers()
    if customers:
        msg = "\n".join([f"ID: {c[0]} | Name: {c[1]} | Balance: {c[2]}" for c in customers])
        messagebox.showinfo("All Customers", msg)
    else:
        messagebox.showinfo("All Customers", "No customers found.")

tk.Button(root, text="Create Account", command=create_account, width=25).pack(pady=5)
tk.Button(root, text="Deposit", command=deposit, width=25).pack(pady=5)
tk.Button(root, text="Withdraw", command=withdraw, width=25).pack(pady=5)
tk.Button(root, text="View Balance", command=view_balance, width=25).pack(pady=5)
tk.Button(root, text="View Transactions", command=view_transactions, width=25).pack(pady=5)
tk.Button(root, text="All Customers", command=all_customers, width=25, bg="lightblue").pack(pady=10)

root.mainloop()
