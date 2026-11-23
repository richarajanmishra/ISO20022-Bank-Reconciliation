# balance_check.py
# Day 2 balance check, written in Python

account = "USD"
statement_date = "09/10/2026"

opening_balance = 4412297.06
credits = 1372048.66
debits = 608136.82
closing_on_statement = 5176208.90

calculated_closing = opening_balance + credits - debits
difference = round(closing_on_statement - calculated_closing, 2)
check = difference == 0

print("Account:", account)
print("Date:", statement_date)
print("Calculated closing:", round(calculated_closing, 2))
print("Closing on statement:", closing_on_statement)
print("Difference:", difference)
print("Check passed:", check)
