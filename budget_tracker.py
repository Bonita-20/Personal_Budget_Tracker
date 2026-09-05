import json
import os
import datetime as dt

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

print("=" * 5 + " " + "BUDGET TRACKER" + " " + "=" * 5)

DATA_FILE = "budget_data.json"
transactions = []

def load_data():
    global transactions
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                transactions = json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: could not read existing data file. Starting fresh.")
            transactions = []


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=2)

# this function splits the categories by income and expense.
def Category(type):
    if type == "Income":
        print("[1] Salary")
        print("[2] Sales")
        print("[3] Gift")
        print("[4] Pension")
        print("[5] Others")

        choice = input("Select an option (1 - 5): ").strip()

        if choice == '1': return 'Salary'
        elif choice == '2': return 'Sales'
        elif choice == '3': return 'Gift'
        elif choice == '4': return 'Pension'
        elif choice == '5': return 'Others'
        else:
            print("Invalid Choice. Please select a number between 1 and 5.")
    else:
        print("[1] Utility")
        print("[2] Transportation")
        print("[3] Debt")
        print("[4] Food")
        print("[5] Rent") 
        print("[6] HealthCare")
        print("[7] Savings")
        print("[8] Family")
        print("[9] Subscription")
        print("[10] Others")      

        choice = input("Select an option (1 - 10): ").strip()

        if choice == '1': return 'Utility'
        elif choice == '2': return 'Transportation'
        elif choice == '3': return 'Debt'
        elif choice == '4': return 'Food'
        elif choice == '5': return 'Rent'
        elif choice == '6': return 'HealthCare'
        elif choice == '7': return 'Savings'
        elif choice == '8': return 'Family'
        elif choice == '9': return 'Subscription'
        elif choice == '10': return 'Others'
        else:
            print("Invalid Choice. Please select a number between 1 and 10.")

# define the function that adds the user transaction.
def add_transaction(type):
    type = type.title()
    print(f"\n--- Add {type} ---")

    category = Category(type)
    description = input("Enter a description (e.g: Lunch, Gift from mum): ").strip()
    if not description:
        description = 'Unspecified'
    while True:
        amount = input("Enter Amount: ").strip()
        try:
            amount = round(float(amount), 2)
            if amount < 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("This is not a valid amount. Enter a valid amount.")

    transaction = {"Type": type, "Category": category, "Description": description, "Amount": amount, "Date": dt.date.today().isoformat()}    
    transactions.append(transaction)
    save_data()
    print(f"\n{type} of {amount} added under {category} successfully.")

# this function view all the transactions that have been added by the user.
def view_all():
    print("\n--- All Transactions ---")
    if not transactions:
        print("No transaction history.")
        return
    print(f"{'Date':<12}{'Type':<10}{'Category':<15}{'Amount':>10}     Description")
    sorted_transaction = sorted(transactions, key=lambda t: t['Date'])
    for transaction in sorted_transaction:
        color = GREEN if transaction['Type'] == "Income" else RED
        print(
            f"{transaction['Date']:<12}"
            f"{transaction['Type']:<10}"
            f"{transaction['Category']:<15}"
            f"{color}{transaction['Amount']:>10.2f}{RESET}    "
            f"{transaction['Description']}"
        )

# this function get the summary of all the transaction
def get_summary():
    print("\n--- SUMMARY ---")
    if not transactions:
        print("No transactions history.")
        return
    total_income = sum(trans['Amount'] for trans in transactions if trans['Type'] == "Income")
    total_expense = sum(trans['Amount'] for trans in transactions if trans['Type'] == "Expense")
    balance = total_income - total_expense
    status = "Surplus" if balance >= 0 else "Deficit"

    print(f"Total Income: {total_income:>10.2f}")
    print(f"Total Expenses: {total_expense:>10.2f}")
    print("-" * 20)
    print(f"Balance ({status}): {balance:>10.2f}")

# this function helps the user to view transaction by category under income or expense
def view_by_category():
    print("\n--- View by Category ---")
    if not transactions:
        print("No transactions history.")
        return

    print("[1] Income by category")
    print("[2] Expenses by category")
    choice = input("Choose an option: ").strip()

    t_type = "income" if choice == "1" else "expense" if choice == "2" else None
    if t_type is None:
        print("Invalid choice.")
        return

    totals = {}
    for t in transactions:
        if t["Type"] == t_type.capitalize():
            totals[t["Category"]] = totals.get(t["Category"], 0) + t["Amount"]

    if not totals:
        print(f"No {t_type} transactions recorded yet.")
        return

    grand_total = sum(totals.values())
    print(f"\n{'Category':<20}{'Amount':>12}{'Percent':>10}")
    print("-" * 42)
    for category, amount in sorted(totals.items(), key=lambda x: -x[1]):
        percent = (amount / grand_total) * 100 if grand_total else 0
        print(f"{category:<20}${amount:>10.2f}{percent:>9.1f}%")
    print("-" * 42)
    print(f"{'Total':<20}${grand_total:>10.2f}")

load_data()

while True:
    print("\nMain Menu:")
    print("[1] Add Income")
    print("[2] Add Expense")
    print("[3] View All Transaction")
    print("[4] Summary")
    print("[5] By Category")
    print("[6] Exit")
    print("\n")

    # collect user choice
    choice = input("Select an option (1 - 6): ").strip()

    if choice == "1":
        add_transaction("income")
    elif choice == "2":
        add_transaction("expense")
    elif choice == "3":
        view_all()
    elif choice == "4":
        get_summary()
    elif choice == "5":
        view_by_category()
    elif choice == "6":
        print("\nGoodbye. Your transaction has been recorded.")
        break
    else:
        print("Invalid choice. Please select a number between 1 and 6.")
