# tracker script
import csv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
class transaction:
    def __init__(self,date,category,description,amount):
        self.date=date
        self.category=category
        self.description=description
        self.amount=amount
    def to_list(self):
        return[self.date,self.category,self.description,self.amount]    
class budget_tracker:
    def __init__(self,transaction):
        self.transaction=[]
    def add_transaction(self,trasaction):
        self.transaction.append(transaction)
    def save_to_csv(self,filename='data/transaction.csv'):
        with open(filename,'w',newline='') as file:
           writer=csv.writer(file)
           writer.writerow(['Date','Category','Description','Amount']) 
        for t in self.transaction:
            writer.writerow(t.to_list())
    def load_from_csv(self,filename='data/transaction.csv'):
        try:
            df=pd.read_csv(filename)
            for _, row in df.iterrows():
                t=transaction(row['Date'],row['Category'],row['Description'],row['Amount'])
                self.transactions.append(t)
        except:
            print("No existing data found, Starting fresh.")
    def summarize_by_category(self):
        df=pd.DataFrame([t.to_list() for t in self.transaction],
                        columns=['Date','Category','Description','Amount'])
        df=['Amount']=pd.to_numeric(df['Amount'], errors='coerce')
        summary=df.groupby('Category')['Amount'].sum()   
        return summary              
    def summarize_by_month(self):
        if not self.transaction:
            return("No transaction to summarize")
        df=pd.DataFrame([t.to_list() for t in self.transaction],
                        columns=['Date','Category','Description','Amount'])
        df=['Date']=pd.to_datetime(df['Date'], errors='coerce')
        df=['Amount']=pd.to_numeric(df['Amount'], errors='coerce')
        df=['Month']=df['Date'].dt.to_period('M')
        summary=df.groupby(['Month','Category'])['Amount'].sum().reset_index()
        return summary
    def plot_monthly_summary(self):
        if not self.transactions:
          print("No transactions to visualize.")
          return

        df = pd.DataFrame([t.to_list() for t in self.transactions],
                      columns=['Date', 'Category', 'Description', 'Amount'])

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Month'] = df['Date'].dt.to_period('M').astype(str)

        summary = df.groupby(['Month', 'Category'])['Amount'].sum().unstack(fill_value=0)

        summary.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title("Monthly Spending by Category")
        plt.xlabel("Month")
        plt.ylabel("Amount (₹)")
        plt.legend(title="Category")
        plt.tight_layout()
        plt.show()
  
import json

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.budget_limits = {}  # e.g., {'Food': 3000, 'Rent': 5000}
    def load_budget_limits(self, filename='data/budget_limits.json'):
      try:
          with open(filename, 'r') as f:
              self.budget_limits = json.load(f)
      except FileNotFoundError:
          print("No budget limits file found. Starting with empty limits.")
    def save_budget_limits(self, filename='data/budget_limits.json'):
        with open(filename, 'w') as f:
            json.dump(self.budget_limits, f, indent=4)
    def check_budget_alerts(self, month):
      df = pd.DataFrame([t.to_list() for t in self.transactions],
                        columns=['Date', 'Category', 'Description', 'Amount'])
  
      df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
      df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
      df['Month'] = df['Date'].dt.to_period('M').astype(str)
  
      month_df = df[df['Month'] == month]
      summary = month_df.groupby('Category')['Amount'].sum()
  
      print(f"\n📊 Budget Check for {month}:")
      for category, spent in summary.items():
          limit = self.budget_limits.get(category)
          if limit:
              if spent > limit:
                  print(f"  ❌ {category}: ₹{spent:.2f} (Over budget! Limit: ₹{limit})")
              else:
                  print(f"  ✅ {category}: ₹{spent:.2f} (Within budget)")
          else:
              print(f"  ⚠️ {category}: ₹{spent:.2f} (No limit set)")     
