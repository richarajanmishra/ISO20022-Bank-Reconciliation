# Project 1 — ISO 20022 Bank Reconciliation

A multi-currency bank reconciliation built from camt.053 XML bank statements for Severn Group, a fictional UK financial services company.

## What It Does

- Parses 15 ISO 20022 camt.053 XML bank statements using Python (xml.etree, pandas), extracting 1,407 multi-currency transactions into a structured CSV
- Matches bank transactions against the cash ledger using a 4-tier matching engine, achieving a 96.6% automated match rate across GBP, USD, and EUR
- Investigates and categorises all 48 breaks — 33 caused by missing end-to-end references, 15 by bank fees with no ledger counterpart
- Produces a 3-page Power BI dashboard with match-rate KPIs, break ageing analysis, and multi-currency cash position reporting

## Folder Structure

```
Severn_P1_Bank_Reconciliation/
│
├── 01_data/
│   ├── bank_transactions.csv        # Parsed output — 1,407 transactions
│   ├── cash_ledger.csv              # Internal cash ledger for matching
│   ├── fx_rates.csv                 # Static FX rates (GBP, USD, EUR)
│   ├── legacy_flat_statement.csv    # Pre-XML flat bank statement
│   └── camt053/                     # 15 raw ISO 20022 XML files
│
├── 02_scripts/
│   ├── parse_camt053.py             # Parses XML → bank_transactions.csv
│   ├── parse_step5.py               # Additional parsing logic
│   └── balance_check.py             # Validates opening/closing balances
│
├── 03_workbook/
│   ├── P1_Reconciliation.xlsx       # 4-tier matching engine
│   ├── Breaks_20261110.xlsx         # 48 unmatched items with categories
│   └── severn_recon.db              # SQLite database for break queries
│
├── 04_dashboard/
│   ├── P1_Bank_Rec.pbix             # Power BI dashboard (3 pages)
│   ├── Overview.png                 # Dashboard screenshot — Overview
│   ├── Breaks.png                   # Dashboard screenshot — Breaks
│   └── CashPosition.png            # Dashboard screenshot — Cash Position
│
├── 05_docs/
│   ├── P1_Portfolio_Memo.docx       # Full project memo
│   ├── README.md                    # This file
│   ├── matching_policy.md           # Matching rules and tier definitions
│   └── signoff_checklist.md         # Completion checklist
│
└── 06_log/
    └── P1_log.docx                  # Daily progress log (Days 1–10)
```

## How to Run

### Prerequisites
- Python 3.x
- pandas (`pip install pandas`)
- Power BI Desktop (for the .pbix file)

### Steps

1. **Parse the XML files**
   ```
   python 02_scripts/parse_camt053.py
   ```
   This reads all 15 camt.053 files from `01_data/camt053/` and generates `01_data/bank_transactions.csv`.

2. **Run the balance check**
   ```
   python 02_scripts/balance_check.py
   ```
   This validates that opening and closing balances in the XML match the parsed transaction totals.

3. **Open the reconciliation workbook**
   Open `03_workbook/P1_Reconciliation.xlsx` in Excel. The matching engine runs across four tiers and flags unmatched items.

4. **View the dashboard**
   Open `04_dashboard/P1_Bank_Rec.pbix` in Power BI Desktop and click **Refresh** to load the latest data.

## Dashboard

### Overview
![Overview](04_dashboard/Overview.png)

### Breaks Analysis
![Breaks](04_dashboard/Breaks.png)

### Cash Position
![Cash Position](04_dashboard/CashPosition.png)

## Tools Used

| Tool | Purpose |
|------|---------|
| Python | XML parsing (xml.etree), data manipulation (pandas) |
| SQL (SQLite) | Break querying and analysis |
| Excel (VBA) | 4-tier matching engine |
| Power BI (DAX) | Dashboard — KPIs, ageing analysis, cash position |

## Key Results

| Metric | Value |
|--------|-------|
| Transactions processed | 1,407 |
| Match rate (Tiers 1–3) | 96.6% |
| Unmatched breaks | 48 |
| Top break cause | Missing end-to-end reference (69% of breaks) |
| Currencies covered | GBP, USD, EUR |

## Scope

This is a portfolio project using fictional data. It demonstrates a complete bank reconciliation workflow — from raw ISO 20022 XML parsing through to dashboard reporting — and is not a production system. All company names, transaction amounts, and counterparties are fictional.

## Author

**Richa Rajan Mishra**
MSc Finance & Investment — University of Bristol
