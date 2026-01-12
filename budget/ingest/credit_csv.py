import csv
from decimal import Decimal
from datetime import datetime
from pathlib import Path

from budget.models.credit_transaction import CreditTransaction
from budget.config.envelope_map import ENVELOPE_MAP


# Possible column name variants seen in CC CSVs
DESC_COLUMNS = [
    "Description",
    "Transaction Description",
    "Merchant",
    "Merchant Name",
    "Details",
    "Payee",
]


AMOUNT_COLUMNS = [
    "Amount",
    "Transaction Amount",
    "Charge Amount",
]

DATE_COLUMNS = [
    "Date",
    "Transaction Date",
    "Posted Date",
]


def _find_column(row: dict, candidates: list[str]) -> str:
    for c in candidates:
        if c in row:
            return c
    raise KeyError(f"None of these columns found: {candidates}")


def load_credit_csv(path: Path, statement_month: str) -> list[CreditTransaction]:
    txns: list[CreditTransaction] = []

    with path.open(encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Peek first row to resolve headers
        first_row = next(reader)
        desc_col = _find_column(first_row, DESC_COLUMNS)
        amt_col = _find_column(first_row, AMOUNT_COLUMNS)
        date_col = _find_column(first_row, DATE_COLUMNS)

        # Process first row + rest
        rows = [first_row] + list(reader)

        for row in rows:
            desc = row[desc_col]
            amt = Decimal(row[amt_col])

            envelope = "Discretionary_Misc"
            for key, env in ENVELOPE_MAP.items():
                if key.upper() in desc.upper():
                    envelope = env
                    break

            txns.append(
                CreditTransaction(
                    date=datetime.strptime(row[date_col], "%m/%d/%Y").date(),
                    description=desc,
                    amount=abs(amt),  # charges always positive
                    envelope=envelope,
                    statement_month=statement_month,
                )
            )

    return txns
