# 💰 Personal Budget Tracker — CLI

A command-line personal finance application built with **Python** for recording income and expenses, monitoring available balances, viewing transaction history, and analysing spending by category.

The project was developed to strengthen practical Python skills including **data structures, functions, control flow, input validation, file handling, JSON persistence, sorting, filtering, and data aggregation**.

---

## 📌 Overview

The **Personal Budget Tracker** provides a simple way to manage personal finances directly from the terminal.

Users can:

* Record income
* Record expenses
* Assign transactions to categories
* Track expenses against specific income sources
* Prevent spending beyond available balances
* View income and expense history
* Generate financial summaries
* Analyse transactions by category
* Persist transaction data between sessions

Transaction data is stored locally in a JSON file, allowing records to remain available after the application is closed.

---

## ✨ Features

| Feature                    | Description                                                |
| -------------------------- | ---------------------------------------------------------- |
| 💵 **Add Income**          | Record income with category, description, amount, and date |
| 💸 **Add Expense**         | Record expenses and associate them with an income source   |
| 🧾 **Transaction History** | View income, expenses, or all transactions                 |
| 📊 **Financial Summary**   | Calculate total income, expenses, and current balance      |
| 📁 **Category Analysis**   | Aggregate transactions by category                         |
| 💾 **Data Persistence**    | Save and load transactions using JSON                      |
| 🛡️ **Input Validation**   | Validate amounts and prevent invalid transactions          |
| 💰 **Balance Tracking**    | Monitor remaining balances for income sources              |
| 📅 **Automatic Dates**     | Automatically record the date of each transaction          |

---

## 🖥️ Application Menu

```text
========================================
          BUDGET TRACKER
========================================

Main Menu:

[1] Add Income
[2] Add Expense
[3] View Transaction
[4] Summary
[5] By Category
[6] Exit
```

The application runs continuously until the user selects **Exit**.

---

## 💵 Income Management

Income can be recorded under the following categories:

```text
1. Salary
2. Sales
3. Gift
4. Pension
5. Others
```

Each income transaction contains:

```python
{
    "Type": "Income",
    "Category": "Salary",
    "Description": "Monthly salary",
    "Amount": 250000.00,
    "Date": "2026-09-23"
}
```

If an invalid category is selected, the application automatically assigns the transaction to **Others**.

---

## 💸 Expense Management

Expenses can be recorded under:

```text
1. Utility
2. Transportation
3. Debt
4. Food
5. Rent
6. HealthCare
7. Savings
8. Family
9. Subscription
10. Others
```

An expense is associated with an existing income category.

For example:

```text
Salary Balance: ₦250,000

Food Expense: ₦5,000

Remaining Salary Balance: ₦245,000
```

The application checks the available balance before recording an expense and cancels the transaction if the requested expense exceeds the available balance.

---

## 📊 Financial Summary

The summary calculates:

```text
Total Income
Total Expenses
Balance
Balance Status
```

The balance is calculated as:

```text
Balance = Total Income - Total Expenses
```

Example:

```text
--- SUMMARY ---

Total Income:      250,000.00
Total Expenses:     87,500.00
----------------------------
Balance (Surplus): 162,500.00
```

The application identifies the balance as either **Surplus** or **Deficit**.

---

## 📁 Category Analysis

Transactions can be grouped and analysed by category.

The user can select:

```text
[1] Income by category
[2] Expenses by category
```

The application then calculates:

* Total amount per category
* Percentage contribution of each category
* Grand total

Example:

```text
Category                 Amount   Percent
------------------------------------------
Food                   15,000.00      35.7%
Transportation           8,000.00      19.0%
Utility                 12,000.00      28.6%
Others                   7,000.00      16.7%
------------------------------------------
Total                  42,000.00
```

This feature demonstrates a fundamental **group-by and aggregation** pattern commonly used in data analysis.

---

## 🧾 Transaction History

The application provides three transaction views:

### Income

```text
--- All Incomes ---

Date        Category           Amount    Description
2026-09-23  Salary          250000.00    Monthly salary
```

### Expenses

```text
--- All Expenses ---

Date        Category           Amount    Description
2026-09-23  Food              5000.00    Lunch
```

### All Transactions

```text
--- All Transactions ---

Date        Type      Category          Amount    Description
2026-09-23  Income    Salary          250000.00   Monthly salary
2026-09-23  Expense   Food              5000.00    Lunch
```

Transactions are sorted by date before being displayed.

---

## 💾 Data Persistence

Transaction data is stored locally in:

```text
budget_data.json
```

The application:

1. Checks whether the JSON file exists.
2. Loads existing transactions when the program starts.
3. Updates the transaction list when new records are added.
4. Saves the updated list back to the JSON file.

The program also handles JSON decoding and file I/O errors when loading existing data.

---

## 🗂️ Project Structure

```text
personal-budget-tracker/
│
├── budget_tracker.py
├── budget_data.json
└── README.md
```

### `budget_tracker.py`

Main Python application containing the menu system and transaction-management functions.

### `budget_data.json`

Local JSON file containing saved transaction records.

### `README.md`

Project documentation.

---

## 🛠️ Tech Stack

**Language**

* Python 3

**Python Modules**

* `json`
* `os`
* `datetime`

**Core Concepts**

* Lists
* Dictionaries
* Functions
* Parameters
* Return values
* Conditional statements
* `for` loops
* `while` loops
* List comprehensions
* Generator expressions
* Sorting
* Filtering
* Aggregation
* Exception handling
* File handling
* JSON serialization/deserialization
* String formatting

The current implementation uses `json` for persistence, `os` for file existence checks, and `datetime` for transaction dates.

---

## 🚀 Getting Started

### Prerequisites

Make sure Python 3 is installed on your computer.

Check your Python installation:

```bash
python --version
```

or:

```bash
python3 --version
```

---

### Installation

Clone the repository:

```bash
git clone https://github.com/Bonita-20/personal_budget_tracker.git
```

Navigate into the project:

```bash
cd personal_budget_tracker
```

---

### Run the Application

On Windows:

```bash
python budget_tracker.py
```

On macOS/Linux:

```bash
python3 budget_tracker.py
```

The application will open in the terminal and display the main menu.

---

## 🧪 Example Usage

### Add Income

```text
Select an option (1 - 6): 1

----- Add Income -----

Select an Income category.
[1] Salary
[2] Sales
[3] Gift
[4] Pension
[5] Others

Select an option (1 - 5): 1

Enter a description: Monthly salary
Enter the income amount: 250000

Income of 250,000.00 added under Salary successfully.
```

### Add Expense

```text
Select an option (1 - 6): 2

----- Add Expense -----

Which income category do you want to make expense from? 1

Enter an expense amount: 5000

Expense of 5000.00 taken from Salary added successfully.
```

### View Summary

```text
--- SUMMARY ---

Total Income:     250000.00
Total Expenses:     5000.00
--------------------
Balance (Surplus): 245000.00
```

---

## 🧠 What I Learned

This project helped me practise how to design a small application around structured data.

### 1. Working with Lists and Dictionaries

Transactions are represented as dictionaries and stored inside a list.

```text
List
  ↓
Dictionary
  ↓
Transaction data
```

This provided practical experience working with nested data structures.

### 2. Functional Decomposition

The application is divided into separate functions, with each function responsible for a specific task.

Examples include:

```text
add_income()
add_expense()
view_transaction()
get_summary()
view_by_category()
```

### 3. Data Aggregation

The category analysis feature introduced the idea of grouping records and calculating totals:

```text
Transactions
      ↓
Filter by type
      ↓
Group by category
      ↓
Sum amounts
      ↓
Calculate percentages
```

### 4. File Persistence

I implemented JSON-based persistence so that transaction data can survive between program sessions.

### 5. Input Validation

The application validates monetary input and prevents transactions that would result in spending beyond the available balance.

---

## 🔮 Future Improvements

Planned improvements include:

* [ ] Search transactions
* [ ] Filter transactions by date
* [ ] Filter transactions by category
* [ ] Add monthly budgets
* [ ] Add spending limits
* [ ] Export transactions to CSV
* [ ] Add data visualisation
* [ ] Add unit tests
* [ ] Improve JSON validation
* [ ] Add database support
* [ ] Develop a graphical user interface
* [ ] Add monthly and yearly financial reports

---

## 📈 Project Roadmap

```text
Phase 1
Python CLI
   │
   ├── Income tracking       ✓
   ├── Expense tracking      ✓
   ├── Transaction history   ✓
   ├── Summary               ✓
   ├── Category analysis     ✓
   └── JSON persistence      ✓
          │
          ▼
Phase 2
Enhanced Functionality
   │
   ├── Search & filtering
   └── Date-range reports
          │
          ▼
Phase 3
Data & Analytics
   │
   ├── CSV export
   ├── Data visualisation
   ├── Monthly analytics
   └── Spending trends
          │
          ▼
Phase 4
Application Development
   │
   ├── Database integration
   ├── GUI
   └── Automated testing
```

---

## 👩🏽‍💻 Author

### Nwamaka Precious Chidiebere

**Statistician | Data Analyst | Data Scientist | Python Learner**

I'm building practical Python and data projects as part of my journey into **data science and AI engineering**.

### Connect With Me

* **GitHub:** [@Bonita-20](https://github.com/Bonita-20)
* **LinkedIn:** [Nwamaka Precious Chidiebere](https://linkedin.com/in/chidiebere-nwamaka-precious)

---

## ⭐ Support

If you find this project useful or you're also learning Python, feel free to **star the repository** and explore the code.

---

## 📄 License

This project is currently intended as a learning and portfolio project.
