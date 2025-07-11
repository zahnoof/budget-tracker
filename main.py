#main.py
from tracker import transaction, budget_tracker
from datetime import datetime
import os
import json
import pandas as pd
os.makedirs('data', exist_ok=True)
tracker=budget_tracker()
tracker.load_from_csv()
def add_transaction():
    date=input("Enter date (YYYY-MM-DD) or leave it blank for today")
    if not date:
        date=datetime.today().strftime('%Y-%m-%d')
    category=input("enter category(e.g., Food, Rent, Entertainment):")
    description=input("Enter description:")
    amount=input("Enter amount:")

    try:
        amount=float(amount)
        t=transaction(date, category, description, amount)
        tracker.add_transaction(t)
        print("✅Transaction added.")
    except ValueError:
        print("❌ invalid amount. Please enter a number.")
def view_summary():
    summary= tracker.summarize_by_category()
    print("📊Spending Summary by Category")
    print(summary)
def view_monthly_summary():
        summary=tracker.summarize_by_month()
        if isinstance(summary,str):
            print(summary)
        else:
            print("\n📅Monthly spending summary:")
            for month in summary['Month'].unique():
                print(f"\n Month:{month}")
                month_data=summary[summary['Month']==month]
                for _, row in month_data.iterrows():
                     print(f"  {row['Category']}: ₹{row['Amount']:.2f}")
def show_monthly_chart():
    tracker.plot_monthly_summary()
def load_budget_limits(self, filename='data/budget_limits.json'):
    try:
        with open(filename, 'r') as f:
            self.budget_limits = json.load(f)
    except FileNotFoundError:
        print("No budget limits file found. Starting with empty limits.")
def save_budget_limits(self, filename='data/budget_limits.json'): 
    with open(filename, 'w') as f:
        json.dump(self.budget_limits, f, indent=4)
def set_budget_limits():
    while True:
        category = input("Enter category (or 'done' to finish): ")
        if category.lower() == 'done':
            break
        try:
            limit = float(input(f"Set monthly limit for {category}: ₹"))
            tracker.budget_limits[category] = limit
        except ValueError:
            print("Invalid amount. Try again.")
    tracker.save_budget_limits()

def check_budget():
    month = input("Enter month (YYYY-MM): ")
    tracker.check_budget_alerts(month)
while True:
    print("\n=== Budget Tracker ===")
    print("1. Add Transaction")
    print("2. View Summary by Category")
    print("3. View Monthly Summary")
    print("4. Show Monthly Spending Chart") 
    print("5. Set Budget Limits")
    print("6. Check Budget Alerts")
    print("7. Save & Exit")
    
    choice = input("Choose an option: ")

    if choice == '1':
        add_transaction()
    elif choice == '2':
        view_summary()
    elif choice == '3':
       view_monthly_summary()
    elif choice == '4':
     show_monthly_chart()
    elif choice == '5':
     set_budget_limits()
    elif choice == '6':
        check_budget()
    elif choice == '7':
        tracker.save_to_csv()
        tracker.save_budget_limits()
        print("💾 Data saved. Goodbye!")
        break
    else:
            print("❌ Invalid choice. Try again.")
