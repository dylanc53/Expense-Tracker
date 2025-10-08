import csv               #imports csv module - allows python to read and write csv  
from datetime import datetime   #imports date/time module- grabs current date and time

def add_expense():      #defines a function- all code under this line runs when we call this function
    amount = input("Enter the expense amount: ")  #expense amount
    category = input("Enter the category (Food, Rent, Fun, etc.): ") #expense category
    description = input("Enter a short description: ") #userinput-desc of item
    date = datetime.now().strftime("%Y-%m-%d")       #datetime in csv

    with open("expenses.csv", mode="a", newline="") as file:   #opens expense csv in eppnd mode ("a") with ensure the file close when done
        writer = csv.writer(file)                              #creates a csv write object called writer that can write rows into the csv file
        writer.writerow([date, amount, category, description]) #writes a new row to the csv file with the expense info date,time,amount,category,description

    print("✅ Expense saved!") #prints a confirmed message 
     # 🔹 Live feed
    view_expenses()
    summary_total()
    summary_by_category()

def view_expenses():   #defines a function that displays all saved expenses
    try:      #tries to open expenses.csv in read mode ("r") if file does not exist will get FileNotFoundError
        with open("expenses.csv", mode="r") as file: 
            reader = csv.reader(file) #Creates a CSV reader object that can go through each row of the file.
            print("\nDate        | Amount | Category | Description") 
            print("-"*50)  #Prints column headers and a line of dashes to make it look neat in the console.
            for row in reader:
                print(f"{row[0]} | ${row[1]} | {row[2]} | {row[3]}")  #loops through each row in the csv file and prints it formatted - ow[0] = date, row[1] = amount, row[2] = category, row[3] = description.
    except FileNotFoundError:
        print("No expenses found yet!")   #If the CSV doesn’t exist yet, prints message

def summary_total():
    total = 0
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                total += float(row[1])  # row[1] is the amount
        print(f"\n💰 Total Expenses: ${total:.2f}")
    except FileNotFoundError:
        print("No expenses found yet!")

#calculating how was spent per category
def summary_by_category():
    totals = {}
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[2]
                amount = float(row[1])
                totals[category] = totals.get(category, 0) + amount
        print("\n📊 Expenses by Category:" )
        for cat, amt in totals.items():
            print(f"{cat}: ${amt:.2f}")
    except FileNotFoundError:
        print("No Expenses Found yet!")

def read_budgets():
    budgets = {}
    try:
        with open("budgets.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                budgets[row[0]] = float(row[1])
    except FileNotFoundError:
        pass
    return budgets


    with open("budgets.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["category", "Budget"])
        for cat, amt in budgets.items():
            writer.writerow([cat, amt])
    print("Budgets Updated Successfully!")

def set_budget():
    budgets = read_budgets()  # load existing budgets first
    while True:
        category = input("Enter Category to set/update (or 'done' to finish): ")
        if category.lower() == "done":
            break
        try:
            amount = float(input(f"Enter Budget amount for {category}: $"))
            budgets[category] = amount
        except ValueError:
            print("Please enter a valid number.")

    with open("budgets.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Budget"])
        for cat, amt in budgets.items():
            writer.writerow([cat, amt])

    print("Budgets Updated Successfully!")

#view budget usage
def view_budget_usage():
    budgets = read_budgets()
    if not budgets:
        print("No Budgets set Yet!")
        return

    # calculate expenses by category
    spent = {}
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[2]
                amount = float(row[1])
                spent[category] = spent.get(category, 0) + amount
    except FileNotFoundError:
        pass

    print("\n📊 Budget Usage:")

    for category, budget in budgets.items():
        used = spent.get(category, 0)
        percent = (used / budget * 100) if budget != 0 else 0
        status = "✅" if used <= budget else "⚠️ Over Budget!"
        print(f"{category}: Spent ${used:.2f} / Budget ${budget:.2f} ({percent:.1f}% {status})")


def main():   #defines the main function where the menu and user choices are handled
 while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Summary (Total & By Category)")
        print("4. Set/Update Budgets")
        print("5. View Budget Usage")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summary_total()
            summary_by_category()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            view_budget_usage()
        elif choice == "6":
            print("Goodbye!")
            break   # ✅ this works because it’s INSIDE the while loop
        else:
            print("Invalid choice.")  #ensures valid user choice if not error message

if __name__ == "__main__":   # makes sure main only runs if this files is executed directly not if imported into another python file
    main()
    

