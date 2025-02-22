import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description


class CSV:

    CSV_FILE = "finance_data.csv"
    COLUMS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError: 
            df = pd.DataFrame(columns = cls.COLUMS)
            df.to_csv(cls.CSV_FILE, index=False) 
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMS)
            writer.writerow(new_entry)
        print("Entry added successfully") 
    
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format = CSV.FORMAT) #converts all values to date-time objects and stores back to the same column
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask] # Contains the rows where the above condition was true

        if filtered_df.empty:
            print("No transactions found")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
 
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum() # Filter for incocme rows and select amount column
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum() # Filter for expense rows and select amount column
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df



def add():
    CSV.initialize_csv()
    date = get_date("Enter the date(dd-mm-yy): ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions")
        print("3. Exit")
        choice = input("Enter your choice(1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yy): ")
            end_date = get_date("Enter the end date (dd-mm-yy): ")
            df = CSV.get_transactions(start_date, end_date) # Can use dataframe if you want to plot it later
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1,2 or 3.")


if __name__ == "__main__":
    main()