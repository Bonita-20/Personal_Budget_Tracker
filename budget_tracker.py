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
def Category(TYPE):
    if TYPE == "Income":
        print("Select an Income category.")
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
            print("Invalid Choice. Categories defaulted to others.")
            return "Others"
    else:
        print("Select an expense category.")
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
            print("Invalid Choice. Category defaulted to others.")
            return "Others"

def income_category(transactions):
    categories = []

    for transaction in transactions:
        if transaction['Type'] == "Income":
            category = transaction["Category"]
            if category not in categories:
                categories.append(category)
    return categories

def income_balance(category):
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        if transaction['Type'] == "Income" and transaction["Category"] == category:
            total_income += transaction["Amount"]
        elif transaction["Type"] == "Expense" and transaction.get("Source") == category:
            total_expense += transaction["Amount"]

    return total_income - total_expense

# this function calculates the column width for the tables to be displayed.
def calculate_col_width(transactions, target_columns, spacing=4):
    widths = {}
    for col in target_columns:
        header_len = len(col)
        
        if not transactions:
            widths[col] = header_len + spacing
            continue
            
        lengths = []
        for row in transactions:
            val = row.get(col, '')
            if col == "Amount":
                try:
                    formatted_val = f"₦{float(val):,.2f}"
                except (ValueError, TypeError):
                    formatted_val = str(val)
                lengths.append(len(formatted_val))
            else:
                lengths.append(len(str(val)))
                
        widths[col] = max(header_len, max(lengths)) + spacing
    return widths


# this function adds an income transaction.
def add_income(transactions):
    print("\n----- Add Income -----")
    category = Category("Income")
    description = input("Enter a description (e.g: Monthly Salary, Gift from mum, Sale of clothes): ").strip()
    if not description:
        description = "Unspecified"
    while True:
        amount_str = input("Enter the income amount: ").strip()
        try:
            amount = round(float(amount_str), 2)

            if amount <= 0:
                print("Income amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("This is not a valid amount. Enter a valid amount.")

    transaction = {'Type': 'Income',
                   'Category': category,
                   'Description': description,
                   'Amount': amount,
                   'Date': dt.date.today().isoformat()}
    transactions.append(transaction)
    save_data()
    print(f"Income of ₦{amount:,.2f} added under {category} successfully.")

# this function adds an expense transaction.
def add_expense(transactions):
    print("----- Add Expense -----")
    income_categories = income_category(transactions)
    if not income_categories:
        print("\nNo income has been recorded yet.")
        print("Please add an income before making an expense.")
        return

    available_categories = []

    for category in income_categories:
        balance = income_balance(category)

        if balance > 0:
            available_categories.append([category, balance])

    if not available_categories:
        print("\nYou have no income balance in this category.")
        print("Expense cannot be recorded.")
        return

    print("\n----- Available Categories -----")
    for index, (category, balance) in enumerate(available_categories, start=1):
        print(f"{[index]}{category:<15}{balance:,.2f}")

    while True:
        choice_str = input("Which income category do you want to make expense from? ").strip()
        try:
            choice = int(choice_str)
            if 1 <= choice <= len(available_categories):
                source, available_balance = available_categories[choice - 1]
                break
            else:
                print(f"Invalid option. Please select an option between 1 and {len(available_categories)}.")
        except ValueError:
            print("Invalid input. Please select a valid number.")

    cat = Category("Expense")
    description = input("Enter a description (e.g: Lunch, Transport for work, Nepa Bill): ").strip()
    if not description:
        description = 'Unspecified'
    while True:
        amount_str = input("Enter the expense amount: ").strip()
        try:
            amount = round(float(amount_str), 2)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("This is not a valid amount. Enter a valid amount.")

    if amount > available_balance:
        Deficit = amount - available_balance
        print('\nInsufficient Balance.')
        print(f"\nIncome Category: {source}"
              f"Available Balance: {available_balance:,.2f}"
              f"Expense Amount: {amount:,.2f}"
              f"Deficit: {Deficit}")
        print("\nTransaction Cancelled.")
        return

    transaction = {"Type": "Expense",
                   "Category": cat,
                   "Description": description,
                   "Amount": amount,
                   "Income Source": source,
                   "Date": dt.date.today().isoformat()}
    transactions.append(transaction)
    save_data()
    print(f"Expense of ₦{amount:,.2f} taken from {source} added under {cat} successfully.")
    remaining_balance = available_balance - amount
    print(f"The remaining balance in {source}: ₦{remaining_balance:,.2f}.")

# this function view all the transactions that have been added by the user.
def view_transaction(transactions):
    if not transactions:
        print("No transaction history.")
        return

    sorted_transaction = sorted(transactions, key=lambda t: t['Date'])
    columns = ['Date', 'Type', 'Category', 'Amount', 'Income Source']

    width = calculate_col_width(transactions, columns)

    print("Which transaction do you want to view?")
    print("1. Income")
    print("2. Expenses")
    print("3. All Transaction")

    choice = input("Select an option (1 - 3): ").strip()

    if choice == '1':
        income = [transaction for transaction in sorted_transaction if transaction['Type'] == 'Income']
        if not income:
            print("\nNo Income transaction history.")
            return

        print("\n--- All Incomes ---")
        print(f"{'Date':<{width['Date']}}{'Category':<{width['Category']}}{'Amount':>{width['Amount']}}    Description")
        for transaction in income:
            amount_str = f"₦{float(transaction['Amount']):,.2f}"
            print(
                f"{transaction['Date']:<{width['Date']}}"
                f"{transaction['Category']:<{width['Category']}}"
                f"{amount_str:>{width['Amount']}}    "
                f"{transaction['Description']}"
            )
    elif choice == '2':
            expenses = [transaction for transaction in sorted_transaction if transaction['Type'] == 'Expense']
            if not expenses:
                print("\nNo Expense transaction history.")
                return
            print("\n--- All Expenses ---")
            print(f"{'Date':<{width['Date']}}{'Category':<{width['Category']}}{'Amount':>{width['Amount']}}    {'Income Source':<{width['Income Source']}}    Description")
            for transaction in expenses:
                amount_str = f"₦{float(transaction['Amount']):,.2f}"
                print(
                    f"{transaction['Date']:<{width['Date']}}"
                    f"{transaction['Category']:<{width['Category']}}"
                    f"{amount_str:>{width['Amount']}}"
                    f"    {transaction['Income Source']:<{width['Income Source']}}"
                    f"    {transaction['Description']}"
                )
    elif choice == '3':
        print("\n--- All Transactions ---")
        print(f"{'Date':<{width['Date']}}{'Type':<{width['Type']}}{'Category':<{width['Category']}}{'Amount':>{width['Amount']}}     Description")
        for transaction in sorted_transaction:
            color = GREEN if transaction['Type'] == "Income" else RED
            amount_str = f"₦{float(transaction['Amount']):,.2f}"
            print(
                f"{transaction['Date']:<{width['Date']}}"
                f"{transaction['Type']:<{width['Type']}}"
                f"{transaction['Category']:<{width['Category']}}"
                f"{color}{amount_str:>{width['Amount']}}{RESET}    "
                f"{transaction['Description']}"
        )
    else:
        print("Invalid Choice. Please select a number between 1 -3.")

# this function get the summary of all the transaction
def get_summary(transactions):
    print("\n--- SUMMARY ---")
    if not transactions:
        print("No transactions history.")
        return
    total_income = sum(trans['Amount'] for trans in transactions if trans['Type'] == "Income")
    total_expense = sum(trans['Amount'] for trans in transactions if trans['Type'] == "Expense")
    balance = total_income - total_expense
    status = "Surplus" if balance >= 0 else "Deficit"

    income_str = f"₦{total_income:,.2f}"
    expense_str = f"₦{total_expense:,.2f}"
    balance_str = f"₦{abs(balance):,.2f}" 

    print(f"Total Income:       {income_str}")
    print(f"Total Expenses:     {expense_str}")
    print("-" * 40)
    print(f"Balance ({status}):  {balance_str}")

# this function helps the user to view transaction by category under income or expense
def view_by_category(transactions):
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

    columns = ['Category', 'Amount', 'Percent']

    w = calculate_col_width(transactions, columns)

    grand_total = sum(totals.values())
    print(f"\n{'Category':<{w['Category']}}{'Amount':>{w['Amount']}}{'Percent':>{w['Percent']}}")
    print("-" * 40)
    for category, amount in sorted(totals.items(), key=lambda x: -x[1]):
        percent = (amount / grand_total) * 100 if grand_total else 0
        amount_str = f"₦{amount:,.2f}"
        percent_str = f"₦{percent:,.2f}"
        print(f"{category:<{w['Category']}}{amount_str:>{w['Amount']}}{percent_str:>{w['Percent']}}%")
    print("-" * 40)
    grand_total_str = f"₦{grand_total:,.2f}"
    print(f"{'Total':<{w['Category']}}{grand_total_str:>{w['Amount']}}")

def main():
    load_data()
    while True:
        print("\nMain Menu:")
        print("[1] Add Income")
        print("[2] Add Expense")
        print("[3] View Transaction")
        print("[4] Summary")
        print("[5] By Category")
        print("[6] Exit")
        print("\n")

        # collect user choice
        choice = input("Select an option (1 - 6): ").strip()

        if choice == "1":
            add_income(transactions)
        elif choice == "2":
            add_expense(transactions)
        elif choice == "3":
            view_transaction(transactions)
        elif choice == "4":
            get_summary(transactions)
        elif choice == "5":
            view_by_category(transactions)
        elif choice == "6":
            print("\nGoodbye. Your transaction has been recorded.")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

if __name__ == "__main__":
    main()