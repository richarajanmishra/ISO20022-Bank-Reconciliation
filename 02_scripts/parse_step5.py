# my_parse_camt053.py
# Reads camt.053 bank statements

from pathlib import Path
import xml.etree.ElementTree as ET

# ---- Find the 15 statement files ----
# This script lives in 02_scripts, so going up 2 folders = the project folder
PROJECT = Path(__file__).resolve().parent.parent
XML_FOLDER = PROJECT / "01_data" / "camt053"

print("Looking in:", XML_FOLDER)
files = sorted(XML_FOLDER.glob("*.xml"))
print("Number of files found:", len(files))

# ---- Namespace: the official "surname" of camt.053 tags, nicknamed c ----
NS = {"c": "urn:iso:std:iso:20022:tech:xsd:camt.053.001.08"}

# ---- Open the FIRST file only ----
first_file = files[5]
root = ET.parse(first_file).getroot()
stmt = root.find(".//c:Stmt", NS)

# ---- Read the account details (Acct -> Id -> IBAN, Acct -> Ccy, Acct -> Nm) ----
iban = stmt.findtext("c:Acct/c:Id/c:IBAN", namespaces=NS)
currency = stmt.findtext("c:Acct/c:Ccy", namespaces=NS)
account_name = stmt.findtext("c:Acct/c:Nm", namespaces=NS)

print("File:", first_file.name)
print("IBAN:", iban)
print("Currency:", currency)
print("Account name:", account_name)


# ---- Step 3: read the opening and closing balances ----
balances = {}                                   # empty dictionary

for bal in stmt.findall("c:Bal", NS):           # loop through both <Bal> boxes
    code = bal.findtext("c:Tp/c:CdOrPrtry/c:Cd", namespaces=NS)    # OPBD or CLBD
    amount = float(bal.findtext("c:Amt", namespaces=NS))            # text -> number
    balances[code] = amount                     # store amount under its code

print("All balances:", balances)
print("Opening balance:", balances["OPBD"])
print("Closing balance:", balances["CLBD"])


# ---- Step 4: read every transaction in this statement ----
entries = stmt.findall("c:Ntry", NS)          # list of all <Ntry> boxes
print("\nNumber of transactions:", len(entries))

transactions = []                             # empty list, ready to fill

for ntry in entries:
    transaction = {
        "ntry_ref": ntry.findtext("c:NtryRef", namespaces=NS),
        "amount": float(ntry.findtext("c:Amt", namespaces=NS)),
        "credit_debit": ntry.findtext("c:CdtDbtInd", namespaces=NS),
        "end_to_end_id": ntry.findtext(".//c:EndToEndId", namespaces=NS),
    }
    transactions.append(transaction)          # add it to the list

print("Transactions read:", len(transactions))
print("First transaction:", transactions[0])
print("Last transaction:", transactions[-1])


# ---- Investigation: find every line with reference SEV0000022 ----
print("\nLines with reference SEV0000022:")
for t in transactions:
    if t["end_to_end_id"] == "SEV0000022":
        print(t)

        
# ---- Step 5: prove the statement balances ----
total_credits = 0
total_debits = 0

for t in transactions:
    if t["credit_debit"] == "CRDT":
        total_credits = total_credits + t["amount"]
    else:
        total_debits = total_debits + t["amount"]

calculated_closing = balances["OPBD"] + total_credits - total_debits

print("\n---- Balance check ----")
print("Opening:           ", balances["OPBD"])
print("+ Credits:         ", round(total_credits, 2))
print("- Debits:          ", round(total_debits, 2))
print("= Calculated close:", round(calculated_closing, 2))
print("Statement closing: ", balances["CLBD"])
print("Statement balances:", round(calculated_closing, 2) == balances["CLBD"])
