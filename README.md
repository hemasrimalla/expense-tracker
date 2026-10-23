# Simple Expense Tracker

A menu-driven command-line expense tracker built in Python (Veda Technology, Level 1 - Day 23). It records expenses, saves them to a CSV file, and generates spending summaries.

## Features
- Add an expense (date, category, description, amount) with input validation
- View all expenses in an aligned table
- Category-wise spending summary (with percentage share)
- Total spending report (count, total, average, highest expense)
- Monthly filtering (`YYYY-MM`) with its own table, summary, and report
- Data saved automatically to `expenses.csv` after every addition

## Tools
- Python 3 (standard library only: `csv`, `os`, `datetime`)
- CSV as the persistent data file

## How to Run
```bash
python expense_tracker.py
```
`expenses.csv` ships with 10 sample expenses across September and October 2026, so every report works immediately.

## Project Structure
```
expense-tracker/
├── expense_tracker.py   # main script
├── expenses.csv         # persistent data file
├── README.md
└── .gitignore
```

## Design
- Each expense is a dictionary: `{"date", "category", "description", "amount"}`; all expenses live in a list of dictionaries.
- Storage is separate from calculations:
  - Storage: `load_expenses()`, `save_expenses()`
  - Validation: `validate_amount()`, `validate_date()`, `validate_month()`
  - Calculations: `total_spending()`, `summarize_by_category()`, `filter_by_month()`
  - Display: `display_expenses()`, `show_category_summary()`, `show_total_report()`
- Validation: amount must be a positive number, date must be a valid `YYYY-MM-DD`, category and description cannot be empty.

## Sample Output
```
--- Category-wise Spending Summary ---
Category                 Total     Share
----------------------------------------
Food                   3920.50     40.6%
Bills                  1999.00     20.7%
Shopping               1999.00     20.7%
Entertainment           899.00      9.3%
Transport               850.00      8.8%
----------------------------------------
TOTAL                  9667.50    100.0%

--- Total Spending Report ---
Number of expenses : 10
Total spending     : Rs. 9667.50
Average expense    : Rs. 966.75
Highest expense    : Rs. 1999.00 (Headphones, Shopping, 2026-10-05)
```

## Interview Questions
**1. How would you store expense records?**
As a list of dictionaries in memory (one dictionary per expense), and written to a CSV file so each record is a row with columns date, category, description, amount.

**2. Why should application data be persisted?**
Variables in memory disappear when the program ends. Saving to a file means expenses survive restarts, so the tracker is actually useful over time.

**3. How would you add monthly filtering?**
Dates are stored as `YYYY-MM-DD`, so an expense belongs to a month if its date starts with that `YYYY-MM` prefix. `filter_by_month()` returns the matching expenses, which are then passed to the same summary and report functions.
