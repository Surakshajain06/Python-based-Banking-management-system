import tkinter as tk
from tkinter import messagebox

# ------------------ Backend Logic ------------------
class bankaccount:
    def __init__(self, acc_name, initialAmt):
        self.acc_name = acc_name
        self.bal = initialAmt

    def GetBalance(self):
        return self.bal

    def deposit(self, amt):
        # Deposit with 5% interest (used for customer deposits, not transfers)
        self.bal += (amt * 1.05)
        return f"Deposit complete into {self.acc_name} account.\nNew Balance: {self.bal:.2f}"

    def add_amount(self, amt):
        # Direct add without interest (for transfers)
        self.bal += amt


class savingsAcct(bankaccount):
    def __init__(self, acc_name, initialAmt):
        super().__init__(acc_name, initialAmt)
        self.fee = 5  # Penalty for withdrawal

    def withdrawal(self, amt):
        if self.bal >= amt + self.fee:
            self.bal -= (amt + self.fee)
            return True, f"Withdrawal complete with ₹{self.fee} fee.\nNew Balance: {self.bal:.2f}"
        else:
            return False, "Insufficient balance (including fee)."

    def Transfer(self, acc2, amt):
        success, msg = self.withdrawal(amt)
        if success:
            acc2.add_amount(amt)  # No interest on transfers
            return f"Amount ₹{amt} transferred to {acc2.acc_name}.\nRemaining Balance: {self.bal:.2f}"
        else:
            return msg


# ------------------ GUI Layer ------------------
import tkinter as tk
from tkinter import messagebox

class BankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Account Manager")

        # Store accounts in a dictionary
        self.accounts = {}

        # ---------------- Create Account Section ----------------
        create_frame = tk.LabelFrame(root, text="Create Account", padx=10, pady=10)
        create_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(create_frame, text="Account Name:").grid(row=0, column=0, sticky="w")
        self.account_name_entry = tk.Entry(create_frame)
        self.account_name_entry.grid(row=0, column=1)

        tk.Label(create_frame, text="Initial Amount:").grid(row=1, column=0, sticky="w")
        self.initial_amount_entry = tk.Entry(create_frame)
        self.initial_amount_entry.grid(row=1, column=1)

        tk.Button(create_frame, text="Create Savings Account", command=self.create_account).grid(row=2, column=0, columnspan=2, pady=5)

        # ---------------- Account Actions Section ----------------
        action_frame = tk.LabelFrame(root, text="Account Actions", padx=10, pady=10)
        action_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(action_frame, text="Account Name:").grid(row=0, column=0, sticky="w")
        self.action_account_entry = tk.Entry(action_frame)
        self.action_account_entry.grid(row=0, column=1)

        tk.Label(action_frame, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(action_frame)
        self.amount_entry.grid(row=1, column=1)

        tk.Button(action_frame, text="Deposit", command=self.deposit).grid(row=2, column=0, pady=5)
        tk.Button(action_frame, text="Withdraw", command=self.withdraw).grid(row=2, column=1, pady=5)
        tk.Button(action_frame, text="Check Balance", command=self.check_balance).grid(row=2, column=2, pady=5)

        # ---------------- Transfer Money Section ----------------
        transfer_frame = tk.LabelFrame(root, text="Transfer Money", padx=10, pady=10)
        transfer_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(transfer_frame, text="From Account:").grid(row=0, column=0, sticky="w")
        self.transfer_from_entry = tk.Entry(transfer_frame)
        self.transfer_from_entry.grid(row=0, column=1)

        tk.Label(transfer_frame, text="To Account:").grid(row=1, column=0, sticky="w")
        self.transfer_to_entry = tk.Entry(transfer_frame)
        self.transfer_to_entry.grid(row=1, column=1)

        tk.Label(transfer_frame, text="Amount:").grid(row=2, column=0, sticky="w")
        self.transfer_amount_entry = tk.Entry(transfer_frame)
        self.transfer_amount_entry.grid(row=2, column=1)

        tk.Button(transfer_frame, text="Transfer", command=self.transfer_money).grid(row=3, column=0, columnspan=2, pady=5)

    # ---------------- Functions ----------------
    def create_account(self):
        name = self.account_name_entry.get().strip()
        try:
            amount = float(self.initial_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return
        if name in self.accounts:
            messagebox.showerror("Error", "Account already exists")
            return
        self.accounts[name] = {"balance": amount}
        messagebox.showinfo("Success", f"Account '{name}' created with balance {amount}")

    def deposit(self):
        name = self.action_account_entry.get().strip()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return
        if name not in self.accounts:
            messagebox.showerror("Error", "Account not found")
            return
        self.accounts[name]["balance"] += amount
        messagebox.showinfo("Success", f"Deposited {amount} to '{name}'")

    def withdraw(self):
        name = self.action_account_entry.get().strip()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return
        if name not in self.accounts:
            messagebox.showerror("Error", "Account not found")
            return
        if self.accounts[name]["balance"] < amount:
            messagebox.showerror("Error", "Insufficient balance")
            return
        self.accounts[name]["balance"] -= amount
        messagebox.showinfo("Success", f"Withdrew {amount} from '{name}'")

    def check_balance(self):
        name = self.action_account_entry.get().strip()
        if name not in self.accounts:
            messagebox.showerror("Error", "Account not found")
            return
        balance = self.accounts[name]["balance"]
        messagebox.showinfo("Balance", f"Account '{name}' has balance: {balance}")

    def transfer_money(self):
        from_acc = self.transfer_from_entry.get().strip()
        to_acc = self.transfer_to_entry.get().strip()
        try:
            amount = float(self.transfer_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return

        if from_acc not in self.accounts:
            messagebox.showerror("Error", f"From account '{from_acc}' not found")
            return
        if to_acc not in self.accounts:
            messagebox.showerror("Error", f"To account '{to_acc}' not found")
            return
        if self.accounts[from_acc]['balance'] < amount:
            messagebox.showerror("Error", "Insufficient balance")
            return

        self.accounts[from_acc]['balance'] -= amount
        self.accounts[to_acc]['balance'] += amount

        messagebox.showinfo("Success", f"Transferred {amount} from {from_acc} to {to_acc}")

# ---------------- Run GUI ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()
