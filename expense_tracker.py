import os
import time
import json
from datetime import datetime
from tabulate import tabulate

def get_date():
	while True:
		try:
			date_string = input("Transaction date (YYYY-MM-DD): ")
			valid_date = datetime.strptime(date_string, "%Y-%m-%d")
			return valid_date.strftime("%Y-%m-%d")
		except ValueError:
			print("Please enter a date in the valid format.")
   
def load_expenses():
	try:
		with open("expense_tracker.json", "r") as file:
			return json.load(file)
	except FileNotFoundError or json.JSONDecodeError:
		return {"expenses": []}

def save_expenses(expense_list):
    with open("expense_tracker.json", "w") as file:
        json.dump(expense_list, file, indent=4)

class Expense:
	def __init__(self, amount, category, date, description):
		self.amount = amount
		self.category = category
		self.date = date
		self.description = description
		
	def __str__(self):
		return f"{self.date} | {self.category} | ${self.amount:.2f} | {self.description}"

	def to_dict(self):
		return {
			"amount": self.amount,
			"category": self.category,
			"date": self.date,
			"description": self.description
		}

	@classmethod
	def from_dict(cls, dict):
		amount = dict.get("amount")
		category = dict.get("category")
		date = dict.get("date")
		description = dict.get("description")
		return cls(amount, category, date, description)

class ExpenseTracker:
	def add_expense(self, amount, category, date, description):
		return Expense(amount, category, date, description)

	def view_expenses(self, expense_list):
		if expense_list:
			table = [[exp["date"], exp["category"], f"${exp['amount']:.2f}", exp["description"]] for exp in expense_list]
			print(tabulate(table, headers=["Date", "Category", "Amount", "Description"]))
		else:
			print("No recorded expenses")
		input("Enter anything to continue: ")

	def total_spent(self, expense_list):
		total = 0
		for expense in expense_list["expenses"]:
			total += expense["amount"]
		print(f"Total spent: ${total:.2f}")
		input("Enter anything to continue: ")

	def total_by_category(self, expense_list, category):
		total = 0
		for expense in expense_list["expenses"]:
			if expense["category"].lower() == category.lower():
				total += expense["amount"]

		if total != 0:
			print(f"Total spent in {category.capitalize()}: ${total:.2f}")
		else:
			print(f"No items in {category.capitalize()}")
		input("Enter anything to continue: ")

	def sort_by_date(self, expense_list):
		sorted_expenses = sorted(expense_list["expenses"], key=lambda expense: datetime.strptime(expense["date"], "%Y-%m-%d"))
		return sorted_expenses

	def sort_by_category(self, expense_list):
		sorted_expenses = sorted(expense_list["expenses"], key=lambda expense: expense["category"], reverse=True)
		return sorted_expenses

def main():
	expense_list = load_expenses()
	tracker = ExpenseTracker()

	while True:
		try:
			print(expense_list) # debug print
			print("Weclome to Expense Tracker")
			print("[1] Add Expense")
			print("[2] View Expenses")
			print("[3] Show Total Spent")
			print("[4] Show Total by Category")
			print("[5] Exit")
		
			action = int(input("Choose an option: "))

			if (action <= 0) or (action >= 6):
				print("Please choose an option within the bounds of 1 - 5")
				continue
		except ValueError:
			print("Please enter a number.")

		if action == 1:
			try:
				description = input("Transaction description / name: ").capitalize()
				category = input("Category: ").capitalize()
				amount = float(input("Transaction amount: "))
				date = get_date()

				expense_list["expenses"].append(tracker.add_expense(amount, category, date, description).to_dict())
			except ValueError or UnboundLocalError:
				print("Something went wrong. Try again")
				time.sleep(2)
				break

			print("Expense added successfully")
			time.sleep(2)
		elif action == 2:
			try:
				sort_method = input("Sort by (d)ate or sort by (c)ategory? ").lower()
				if sort_method.startswith("c"):
					sorted_list = tracker.sort_by_category(expense_list)
				elif sort_method.startswith("d"):
					sorted_list = tracker.sort_by_date(expense_list)
				else:
					print("Invalid sorting method. Defaulting to date.")
					sorted_list = tracker.sort_by_date(expense_list)
			except ValueError:
				print("Please enter a value.")
    
			tracker.view_expenses(sorted_list)

		elif action == 3:
			tracker.total_spent(expense_list)
		elif action == 4:
			try:
				requested_category = input("Total for category: ").capitalize()
			except ValueError:
				print("Please enter a category")

			tracker.total_by_category(expense_list, requested_category)
		else:
			save_expenses()
			break

		os.system("cls")

if __name__ == "__main__":
	main()