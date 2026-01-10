# Phase 1 — Data Intake (Authoritative)
Objective

Convert raw Bank of America CSVs into a single, trustworthy transaction ledger that reflects economic reality according to Phase 0 rules.

If the ledger is wrong, nothing else matters.

## 1. Supported Inputs (Explicit)

Bank of America CSV exports

Accounts included:

Checking

Savings

Credit card

Time range:

Any (system must support incremental imports)

Non-goal:
Live sync, APIs, partial statements, screenshots.

## 2. Normalization Rules (No Exceptions)
Unified Transaction Ledger

All imported data becomes one list of transactions with a consistent structure.

Each transaction must have:

Date (posted date)

Description (raw, unmodified)

Amount (signed)

Source account type (checking / savings / credit)

Unique internal ID

If any of these are missing, the import is invalid.

## 3. Amount Semantics (This is critical)

Income: positive amount

Spending: negative amount

Transfers: signed amounts but ignored by budgeting logic

You do NOT “fix” signs later.
If amounts are inconsistent, they are normalized on import.

## 4. Account Merging Rule

Checking + Savings are merged into a single Cash Pool

Internal transfers between them are flagged as transfer

These transfers:

Do not affect Cash Pool totals

Do not affect envelopes

Exist only for reconciliation

If a transaction moves money within BoA-owned cash accounts, it is noise.

## 5. Transfer Detection (Minimum Viable Logic)

The system must identify and flag:

Checking ↔ Savings transfers

Credit card payments

Any transaction explicitly marked as transfer by the user

Transfer detection can be imperfect initially, but:

It must be correctable

Corrections must persist across imports

## 6. Credit Card Intake Rules

Credit card CSVs are imported alongside cash accounts

Credit card transactions are not merged into Cash Pool

Credit card purchases:

Are imported as spending

Increase credit liability

Credit card payments:

Are imported as transfers

Reduce Cash Pool

Reduce credit liability

If credit data is missing or delayed, projections are untrusted.

## 7. Deduplication & Idempotency

Re-importing the same CSV must:

Not duplicate transactions

Not change previously classified transactions

Not reset manual corrections

If you can’t safely re-import, your workflow is fragile.

## 8. Validation Checks (Hard Gates)

An import is only considered valid if:

Total Cash Pool balance matches bank reality (± timing gaps)

Credit card balance matches statement balance

No transaction is unclassified (income / spending / transfer)

Internal transfers do not change net totals

Ledger math balances

If any check fails, the import is rejected or flagged.

## 9. User Corrections (Required)

The system must support:

Reclassifying transaction type

Marking / unmarking transfers

Editing descriptions (optional)

Persisting corrections permanently

If corrections are lost, the system is unusable.

## 10. Phase 1 Acceptance Criteria

You are done with Phase 1 only when:

You can import:

Checking CSV

Savings CSV

Credit card CSV

The system produces:

One unified ledger

Correct Cash Pool total

Correct credit liability

Transfers do not distort totals

Re-importing does not break anything

You trust the numbers without mental gymnastics