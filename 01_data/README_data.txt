SEVERN GROUP - PROJECT 1 DUMMY DATA (fictional; no real company or person)
Period: Mon 5 Oct - Fri 9 Oct 2026 (5 banking days)

Bank accounts (reconcile each in its OWN currency):
  GB29SEVN60161331926819  GBP  Severn UK - Operating GBP
  GB54SEVN60161331926820  EUR  Severn UK - Collections EUR
  US11SEVN00012345678901  USD  Severn US - Operating USD
Group reporting currency: GBP (convert only for the daily group cash position).
INR is not used in Project 1 - Severn India appears in Project 4 (month-end close).

Files:
  camt053/                 15 ISO 20022 camt.053 statements (3 accounts x 5 days)
  cash_ledger.csv          1,400 cash ledger entries (receipts and payments)
  legacy_flat_statement.csv same bank data, old-style: date, amount, short narrative only
  fx_rates.csv             daily GBP/EUR and GBP/USD rates (units of currency per 1 GBP)
  ANSWER_KEY_...csv        104 planted issues - DO NOT OPEN until Day 7, then check your results

Key camt.053 fields per <Ntry>: NtryRef, Amt (+Ccy), CdtDbtInd (CRDT in / DBIT out),
BookgDt, EndToEndId, Dbtr/Cdtr Nm, RmtInf/Ustrd.
Ledger end_to_end_id matches the bank EndToEndId where the payer provided it.

Severn Group: ISO 20022 Bank Reconciliation
Portfolio simulation using dummy data only. No real company, employer or client data is used.

Business problem
Finance teams reconcile bank accounts to the cash ledger every day to prove that cash is correct and to catch errors, missing payments and fraud early. Much of this work is still manual because traditional bank statements carry very little information. Banks now send statements in the ISO 20022 (camt.053) format, which includes richer data such as unique payment references and remittance details. This project tests how much of the matching that extra data can automate, and how a cash team should manage what is left.

Scope

Fictional group: Severn Group (UK, US and India entities), reporting in GBP
Bank accounts: GBP operating (Severn UK), EUR collections (Severn UK), USD operating (Severn US)
Period: 5–9 October 2026 (5 banking days)
Data: 15 camt.053 statements (1,407 bank lines) and a cash ledger (1,400 entries)

Tools
Excel (SUMIFS, PivotTables, VBA), Python (pandas), SQL (SQLite), Power BI

Progress

Day 1: Defined the Severn Group setting and wrote a matching policy (4 match tiers, tolerances, break categories, ageing and escalation, four-eyes controls).
Day 2: Validated the source data. All 15 statements balance (opening + credits − debits = closing), and each day’s opening balance equals the previous day’s closing balance. Ledger: 460 EUR, 470 GBP and 470 USD entries.
