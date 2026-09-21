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

        choice = input("Select an option (1 - 4): ").strip()

        if choice == '1': return 'Salary'
        elif choice == '2': return 'Sales'
        elif choice == '3': return 'Gift'
        elif choice == '4': return 'Pension'
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

        choice = input("Select an option (1 - 9): ").strip()

        if choice == '1': return 'Utility'
        elif choice == '2': return 'Transportation'
        elif choice == '3': return 'Debt'
        elif choice == '4': return 'Food'
        elif choice == '5': return 'Rent'
        elif choice == '6': return 'HealthCare'
        elif choice == '7': return 'Savings'
        elif choice == '8': return 'Family'
        elif choice == '9': return 'Subscription'
        else:
            print("Invalid Choice. Category defaulted to others.")
            return "Others"

def income_category():
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

# this function that adds the user transaction.
def add_transaction(TYPE):
    TYPE = TYPE.title()
    print(f"\n--- Add {TYPE} ---")

    source = None

    if TYPE == "Expense":
        income_categories = income_category()

        if not income_categories:
            print("\nNo income has been recorded yet.")
            print("Please add an income before making an expense.")
            return

        available_categories = []

        for category in income_categories:
            balance = income_balance(category)

            if balance > 0:
                available_categories.append((category, balance))

        if not available_categories:
            print("\nYou have no income balance in this category.")
            print("Expense cannot be recorded.")
            return

        print("\nAvailable Income Categories:")
        for index, (category, balance) in enumerate(available_categories, start=1):
            print(f"[{index}] {category:<15} {balance:,.2f}")

        while True:
            choice = input("\nWhich income category do you want to deduct from? ").strip()
            try:
                choice = int(choice)
                if 1 <= choice <= len(available_categories):
                    source, available_balance = available_categories[choice - 1]
                    break
                else:
                    print(f"Invalid choice. Select a number between 1 and {len(available_categories)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")   

    category = Category(TYPE)
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

    if TYPE == "Expense":
        if amount > available_balance:
            Deficit = amount - available_balance

            print("\n" + "=" * 20)
            print("Insufficient Balance")
            print("=" * 20)

            print(f"Income Category:    {source}")
            print(f"Available Balance:    {available_balance:,.2f}")
            print(f"Expense Amount:    ₦{amount:,.2f}")
            print(f"Deficit:    {Deficit:,.2f}")

            print("\nTransaction cancelled.")
            return

    transaction = {"Type": TYPE, "Category": category, "Description": description, "Amount": amount, "Date": dt.date.today().isoformat()} 
    if TYPE == "Expense":
        transaction["Source"] = source

    transactions.append(transaction)
    save_data()
    print(f"\n{TYPE} of ₦{amount} added under {category} successfully.")

    if TYPE == "Expense":
        remaining_balance = available_balance - amount

        print(f"Deducted from: {source}")
        print(f"Remaining Balance In {source}:    ₦{remaining_balance:,.2f}")

# this function view all the transactions that have been added by the user.
def view_transaction(transactions):
    if not transactions:
        print("No transaction history.")
        return

    sorted_transaction = sorted(transactions, key=lambda t: t['Date'])

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
        print(f"{'Date':<12}{'Category':<15}{'Amount':>15}    Description")
        for transaction in income:
            print(
                f"{transaction['Date']:<12}"
                f"{transaction['Category']:<15}"
                f"₦{transaction['Amount']:>15.2f}    "
                f"{transaction['Description']}"
            )
    elif choice == '2':
            expenses = [transaction for transaction in sorted_transaction if transaction['Type'] == 'Expense']
            if not expenses:
                print("\nNo Expense transaction history.")
                return
            print("\n--- All Expenses ---")
            print(f"{'Date':<12}{'Category':<15}{'Amount':>15}    Description")
            for transaction in expenses:
                print(
                    f"{transaction['Date']:<12}"
                    f"{transaction['Category']:<15}"
                    f"₦{transaction['Amount']:>15.2f}    "
                    f"{transaction['Description']}"
                )
    elif choice == '3':
        print("\n--- All Transactions ---")
        print(f"{'Date':<12}{'Type':<10}{'Category':<15}{'Amount':>15}     Description")
        for transaction in sorted_transaction:
            color = GREEN if transaction['Type'] == "Income" else RED
            print(
                f"{transaction['Date']:<12}"
                f"{transaction['Type']:<10}"
                f"{transaction['Category']:<15}"
                f"{color}₦{transaction['Amount']:>15.2f}{RESET}    "
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

    print(f"Total Income: ₦{total_income:>10.2f}")
    print(f"Total Expenses: ₦{total_expense:>10.2f}")
    print("-" * 20)
    print(f"Balance ({status}): ₦{balance:>10.2f}")

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

    grand_total = sum(totals.values())
    print(f"\n{'Category':<20}{'Amount':>12}{'Percent':>10}")
    print("-" * 42)
    for category, amount in sorted(totals.items(), key=lambda x: -x[1]):
        percent = (amount / grand_total) * 100 if grand_total else 0
        print(f"{category:<20}₦{amount:>10.2f}{percent:>9.1f}%")
    print("-" * 42)
    print(f"{'Total':<20}₦{grand_total:>10.2f}")

# this function deletes a transaction from the transactions list.
def delete_transaction(transactions):
    if not transactions:
        print("\nNo transaction history.")
        return

    print("\n--- Delete Transaction ---")

    for index, transaction in enumerate(transactions, start=1):
        color = GREEN if transaction["Type"] == "Income" else RED

        source = ""
        if transaction["Type"] == "Expense":
            source = f" | Source: {transaction.get('Source', 'Others')}"

        print(
            f"{index}. "
            f"{transaction['Date']} | "
            f"{transaction['Type']} | "
            f"{transaction['Category']} | "
            f"{color}₦{transaction['Amount']:,.2f}{RESET} | "
            f"{transaction['Description']}"
            f"{source}"
        )

    while True:
        choice = input(
            "\nEnter the transaction number to delete "
            "(or 0 to cancel): "
        ).strip()

        try:
            choice = int(choice)

            if choice == 0:
                print("Deletion cancelled.")
                return

            if 1 <= choice <= len(transactions):
                break

            print(f"Invalid choice. Enter a number between 1 and {len(transactions)}, or 0 to cancel.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    transaction = transactions[choice - 1]

    print("\nSelected Transaction:")
    print(f"Type:        {transaction['Type']}")
    print(f"Category:    {transaction['Category']}")
    print(f"Amount:      ₦{transaction['Amount']:,.2f}")
    print(f"Description: {transaction['Description']}")
    print(f"Date:        {transaction['Date']}")

    if transaction["Type"] == "Expense":
        print(
            f"Source:      "
            f"{transaction.get('Source', 'Others')}"
        )
    # Confirming from the user the deletion
    while True:
        option = input(
            "\nAre you sure you want to delete this transaction? (y/n): "
        ).strip().lower()

        if option == "y":
            deleted_transaction = transactions.pop(choice - 1)
            save_data()

            print("\nTransaction deleted successfully.")

            # Show restored balance for an expense
            if deleted_transaction["Type"] == "Expense":
                source = deleted_transaction.get("Source")

                if source:
                    balance = income_balance(source)

                    print(
                        f"Updated {source} balance: "
                        f"₦{balance:,.2f}"
                    )

            return

        elif option == "n":
            print("Deletion cancelled.")
            return

        else:
            print("Please enter Y or N.")
load_data()

def main():
    while True:
        print("\nMain Menu:")
        print("[1] Add Income")
        print("[2] Add Expense")
        print("[3] View Transaction")
        print("[4] Summary")
        print("[5] By Category")
        print("[6] Delete Transaction")
        print("[7] Exit")
        print("\n")

        # collect user choice
        choice = input("Select an option (1 - 7): ").strip()

        if choice == "1":
            add_transaction("income")
        elif choice == "2":
            add_transaction("expense")
        elif choice == "3":
            view_transaction(transactions)
        elif choice == "4":
            get_summary(transactions)
        elif choice == "5":
            view_by_category(transactions)
        elif choice == "6":
            delete_transaction(transactions)
        elif choice == "7":
            print("\nGoodbye. Your transaction has been recorded.")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

if __name__ == "__main__":
    main()