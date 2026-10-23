"""
Simple Expense Tracker
----------------------
Records expenses (date, category, description, amount), saves them to a
CSV file, and generates spending summaries.

Each expense is stored as a dictionary:
    {"date": "2026-10-05", "category": "Food",
     "description": "Lunch", "amount": 120.50}
All expenses are kept in a list of dictionaries while the program runs.
"""

import csv
import os
from datetime import datetime

DATA_FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]


# ---------------------------------------------------------------
# Data storage (file handling only - no calculations here)
# ---------------------------------------------------------------
def load_expenses(filename=DATA_FILE):
    """Read expenses from the CSV file and return a list of dictionaries.
    Creates the file with a header row if it does not exist."""
    expenses = []
    if not os.path.exists(filename):
        save_expenses(expenses, filename)
        return expenses
    try:
        with open(filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expenses.append({
                        "date": row["date"],
                        "category": row["category"],
                        "description": row["description"],
                        "amount": float(row["amount"]),
                    })
                except (KeyError, ValueError, TypeError):
                    print("Warning: skipped a corrupted row in the data file.")
    except OSError as error:
        print(f"Could not read {filename}: {error}")
    return expenses


def save_expenses(expenses, filename=DATA_FILE):
    """Write the full list of expenses to the CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            for expense in expenses:
                writer.writerow({
                    "date": expense["date"],
                    "category": expense["category"],
                    "description": expense["description"],
                    "amount": f"{expense['amount']:.2f}",
                })
    except OSError as error:
        print(f"Could not save to {filename}: {error}")


# ---------------------------------------------------------------
# Validation
# ---------------------------------------------------------------
def validate_amount(text):
    """Return the amount as a float if it is a positive number, else None."""
    try:
        amount = float(text)
    except ValueError:
        return None
    if amount <= 0 or amount != amount or amount == float("inf"):
        return None
    return round(amount, 2)


def validate_date(text):
    """Return the date string if it is a valid YYYY-MM-DD, else None."""
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return text
    except ValueError:
        return None


def validate_month(text):
    """Return the month string if it is a valid YYYY-MM, else None."""
    try:
        datetime.strptime(text, "%Y-%m")
        return text
    except ValueError:
        return None


# ---------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------
def ask_date():
    """Keep asking until a valid date is entered (blank = today)."""
    while True:
        text = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
        if text == "":
            return datetime.now().strftime("%Y-%m-%d")
        if validate_date(text):
            return text
        print("  Invalid date. Use the format YYYY-MM-DD, e.g. 2026-10-23.")


def ask_text(label):
    """Keep asking until a non-empty value is entered."""
    while True:
        text = input(f"{label}: ").strip()
        if text:
            return text
        print(f"  {label} cannot be empty.")


def ask_amount():
    """Keep asking until a positive number is entered."""
    while True:
        amount = validate_amount(input("Amount: ").strip())
        if amount is not None:
            return amount
        print("  Invalid amount. Enter a positive number, e.g. 250 or 99.50.")


# ---------------------------------------------------------------
# Core features
# ---------------------------------------------------------------
def add_expense(expenses):
    """Collect a new expense from the user, store it, and save the file."""
    print("\n--- Add Expense ---")
    expense = {
        "date": ask_date(),
        "category": ask_text("Category").title(),
        "description": ask_text("Description"),
        "amount": ask_amount(),
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added: {expense['description']} - Rs. {expense['amount']:.2f}")


def display_expenses(expenses, title="All Expenses"):
    """Print expenses in an aligned table."""
    print(f"\n--- {title} ---")
    if not expenses:
        print("No expenses to show.")
        return
    print(f"{'No.':<5}{'Date':<12}{'Category':<15}{'Description':<25}{'Amount':>10}")
    print("-" * 67)
    for number, e in enumerate(expenses, start=1):
        print(f"{number:<5}{e['date']:<12}{e['category']:<15}"
              f"{e['description'][:24]:<25}{e['amount']:>10.2f}")
    print("-" * 67)
    print(f"{'Total':<57}{total_spending(expenses):>10.2f}")


# ---------------------------------------------------------------
# Calculations (no input/output files here)
# ---------------------------------------------------------------
def total_spending(expenses):
    """Return the sum of all expense amounts."""
    return sum(e["amount"] for e in expenses)


def summarize_by_category(expenses):
    """Return a dict {category: total}, sorted from highest to lowest."""
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def filter_by_month(expenses, month):
    """Return only expenses whose date starts with the given YYYY-MM."""
    return [e for e in expenses if e["date"].startswith(month)]


# ---------------------------------------------------------------
# Reports
# ---------------------------------------------------------------
def show_category_summary(expenses, title="Category-wise Spending Summary"):
    """Print total spending per category with percentage share."""
    print(f"\n--- {title} ---")
    if not expenses:
        print("No expenses to summarize.")
        return
    total = total_spending(expenses)
    print(f"{'Category':<18}{'Total':>12}{'Share':>10}")
    print("-" * 40)
    for category, amount in summarize_by_category(expenses).items():
        print(f"{category:<18}{amount:>12.2f}{amount / total * 100:>9.1f}%")
    print("-" * 40)
    print(f"{'TOTAL':<18}{total:>12.2f}{100.0:>9.1f}%")


def show_total_report(expenses, title="Total Spending Report"):
    """Print grand total, count, average, and the largest expense."""
    print(f"\n--- {title} ---")
    if not expenses:
        print("No expenses recorded yet.")
        return
    total = total_spending(expenses)
    biggest = max(expenses, key=lambda e: e["amount"])
    print(f"Number of expenses : {len(expenses)}")
    print(f"Total spending     : Rs. {total:.2f}")
    print(f"Average expense    : Rs. {total / len(expenses):.2f}")
    print(f"Highest expense    : Rs. {biggest['amount']:.2f} "
          f"({biggest['description']}, {biggest['category']}, {biggest['date']})")


def monthly_report(expenses):
    """Ask for a month and show its expenses, summary, and total."""
    month = input("\nEnter month (YYYY-MM): ").strip()
    if not validate_month(month):
        print("Invalid month. Use the format YYYY-MM, e.g. 2026-10.")
        return
    monthly = filter_by_month(expenses, month)
    if not monthly:
        print(f"No expenses found for {month}.")
        return
    display_expenses(monthly, f"Expenses for {month}")
    show_category_summary(monthly, f"Category Summary for {month}")
    show_total_report(monthly, f"Total Report for {month}")


# ---------------------------------------------------------------
# Menu
# ---------------------------------------------------------------
def main_menu():
    """Print the menu options."""
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Category-wise spending summary")
    print("4. Total spending report")
    print("5. Monthly report (filter by month)")
    print("6. Exit")


def main():
    expenses = load_expenses()
    print(f"Loaded {len(expenses)} expense(s) from {DATA_FILE}.")
    while True:
        main_menu()
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            display_expenses(expenses)
        elif choice == "3":
            show_category_summary(expenses)
        elif choice == "4":
            show_total_report(expenses)
        elif choice == "5":
            monthly_report(expenses)
        elif choice == "6":
            print("Goodbye! Your expenses are saved.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
