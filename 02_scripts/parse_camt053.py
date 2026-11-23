# my_parse_camt053.py
# Reads ALL camt.053 bank statements, checks each one balances,
# and collects every transaction into one list.

from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd

# ---- Find the 15 statement files ----
PROJECT = Path(__file__).resolve().parent.parent
XML_FOLDER = PROJECT / "01_data" / "camt053"
files = sorted(XML_FOLDER.glob("*.xml"))
print("Number of files found:", len(files))

NS = {"c": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.08"}

all_transactions = []          # every transaction from every file
statements_passed = 0          # how many statements balance

print("\n---- Statement checks ----")

# ---- OUTER LOOP: one statement file at a time ----
for xml_file in files:
    root = ET.parse(xml_file).getroot()
    stmt = root.find(".//c:Stmt", NS)

    iban = stmt.findtext("c:Acct/c:Id/c:IBAN", namespaces=NS)
    currency = stmt.findtext("c:Acct/c:Ccy", namespaces=NS)

    # Opening and closing balances
    balances = {}
    for bal in stmt.findall("c:Bal", NS):
        code = bal.findtext("c:Tp/c:CdOrPrtry/c:Cd", namespaces=NS)
        balances[code] = float(bal.findtext("c:Amt", namespaces=NS))

    # ---- INNER LOOP: one transaction at a time ----
    total_credits = 0
    total_debits = 0
    for ntry in stmt.findall("c:Ntry", NS):
        amount = float(ntry.findtext("c:Amt", namespaces=NS))
        credit_debit = ntry.findtext("c:CdtDbtInd", namespaces=NS)

        # Payer name (money in) or payee name (money out)
        party_name = ntry.findtext(".//c:Dbtr/c:Nm", namespaces=NS)
        if party_name is None:
            party_name = ntry.findtext(".//c:Cdtr/c:Nm", namespaces=NS)

        transaction = {
            "account_id": iban,
            "currency": currency,
            "ntry_ref": ntry.findtext("c:NtryRef", namespaces=NS),
            "booking_date": ntry.findtext("c:BookgDt/c:Dt", namespaces=NS),
            "amount": amount,
            "credit_debit": credit_debit,
            "end_to_end_id": ntry.findtext(".//c:EndToEndId", namespaces=NS),
            "party_name": party_name,
            "remittance_text": ntry.findtext(".//c:RmtInf/c:Ustrd", default="", namespaces=NS),
        }
        all_transactions.append(transaction)

        if credit_debit == "CRDT":
            total_credits = total_credits + amount
        else:
            total_debits = total_debits + amount

    # Balance check for THIS statement
    calculated_closing = round(balances["OPBD"] + total_credits - total_debits, 2)
    check = calculated_closing == balances["CLBD"]
    if check:
        statements_passed = statements_passed + 1
    print(xml_file.name, "| closing:", balances["CLBD"], "| balances:", check)

# ---- Summary ----
print("\n---- Summary ----")
print("Statements checked:", len(files))
print("Statements that balance:", statements_passed)
print("Total bank lines read:", len(all_transactions))

missing_reference = 0
for t in all_transactions:
    if t["end_to_end_id"] == "NOTPROVIDED":
        missing_reference = missing_reference + 1
print("Lines with no end-to-end reference:", missing_reference)


# ---- Lesson 7: turn the list into a table ----
bank = pd.DataFrame(all_transactions)

print("\n---- Bank table ----")
print("Rows and columns:", bank.shape)
print(bank[["currency", "ntry_ref", "amount", "credit_debit", "end_to_end_id"]].head())



# ---- Lesson 7: turn the list into a table ----
bank = pd.DataFrame(all_transactions)

print("\n---- Bank table ----")
print("Rows and columns:", bank.shape)
print(bank[["currency", "ntry_ref", "amount", "credit_debit", "end_to_end_id"]].tail())



# ---- Lesson 7: turn the list into a table ----
bank = pd.DataFrame(all_transactions)

print("\n---- Bank table ----")
print("Rows and columns:", bank.shape)
print(bank[["currency", "ntry_ref", "amount", "credit_debit", "end_to_end_id"]].head(10))



# ---- Save the bank table as a CSV file ----
OUTPUT = PROJECT / "01_data" / "bank_transactions.csv"
bank.to_csv(OUTPUT, index=False)
print("\nSaved", len(bank), "rows to:", OUTPUT)


# ---- Control check: totals by currency and day (compare with Day 2 Excel) ----
print("\n---- Credits and debits by currency and day ----")
summary = bank.pivot_table(
    index=["currency", "booking_date"],   # rows
    columns="credit_debit",               # columns: CRDT and DBIT
    values="amount",                      # what to add up
    aggfunc="sum",                        # how: sum
).round(2)
print(summary)

print("\n---- Bank lines per currency ----")
print(bank.groupby("currency").size())
