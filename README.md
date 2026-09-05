# Personal Budget Tracker

A simple command-line application for tracking personal income and expenses, built in Python with no external dependencies.

## Features

- **Add Income** — record money coming in, with category, description, and date
- **Add Expense** — record money going out, with category, description, and date
- **View All Transactions** — see every transaction in a sorted table
- **View Summary** — total income, total expenses, and your overall balance (surplus/deficit)
- **View by Category** — breakdown of income or expenses by category, with percentages
- **Persistent storage** — all data is saved automatically to a local JSON file, so it's still there the next time you run the program

## Requirements

- Python 3.6 or higher
- No external packages required (uses only the standard library: `json`, `os`, `datetime`)

## Installation

1. Download `budget_tracker.py` (or copy it into a file of that name).
2. Make sure Python 3 is installed on your system:
   ```bash
   python3 --version
   ```

## Usage

Run the script from your terminal:

```bash
python3 budget_tracker.py
```

You'll see the main menu:

```
Main Menu:
[1] Add Income
[2] Add Expense
[3] View All Transactions
[4] View Summary
[5] View by Category
[6] Exit
```

Enter a number to choose an option, and follow the prompts.

### Adding a transaction

When adding income or an expense, you'll be asked for:

| Field | Required? | Notes |
|---|---|---|
| Amount | Yes | Must be a positive number |
| Category | No | Defaults to "Other" if left blank; suggested categories are shown |
| Description | No | Free text, e.g. "Groceries at Trader Joe's" |
| Date | No | Defaults to the day of entering the transaction. |

### Viewing your data

- **View All Transactions** lists every entry, sorted by date.
- **View Summary** shows total income, total expenses, and your balance.
- **View by Category** lets you choose income or expenses, then shows a ranked breakdown by category with percentages of the total.

## Data Storage

All transactions are saved to a file called `budget_data.json`, created automatically in the same folder where you run the script. Each transaction is stored as an object like this:

```json
{
  "type": "expense",
  "amount": 45.99,
  "category": "Food",
  "description": "Groceries",
  "date": "2026-09-01"
}
```

Data is saved immediately after every new transaction, so nothing is lost if the program closes unexpectedly. On startup, existing data is loaded automatically — just run the script from the same folder each time.

> **Note:** If `budget_data.json` becomes corrupted or is edited incorrectly by hand, the program will print a warning and start with an empty transaction list rather than crashing.

## Project Structure

```
.
├── budget_tracker.py    # Main application
└── budget_data.json     # Auto-generated data file (created on first run)
```

## Possible Improvements

Ideas for extending this project:

- Migrate storage from JSON to SQLite for larger datasets and faster queries
- Add the ability to edit or delete existing transactions
- Filter transactions by date range or month
- Set budget limits per category with alerts when exceeded
- Export data to CSV
- Add a graphical (GUI) or web-based interface

## Author

Chidiebere, Nwamaka Precious

| Statistics | Data Science | Programming
## License

Free to use, modify, and distribute for personal or educational purposes.