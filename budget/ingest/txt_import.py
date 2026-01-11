from datetime import datetime
from decimal import Decimal
from pathlib import Path

from models.transaction import Transaction


def load_bofa_txt(path: Path, account_name: str) -> list[Transaction]:
    """
    Parse a Bank of America TXT statement (fixed-width format).
    """
    transactions: list[Transaction] = []

    with path.open(encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False

    for line in lines:
        line = line.rstrip()

        # Detect start of transaction table
        if line.startswith("Date") and "Description" in line:
            in_table = True
            continue

        if not in_table:
            continue

        # Skip empty lines
        if not line.strip():
            continue

        # Skip beginning balance row
        if "Beginning balance" in line:
            continue

        # Fixed-width slicing (based on observed format)
        # Date:        columns 0–10
        # Description: columns 12–82
        # Amount:      columns 82–96
        try:
            date_str = line[0:10].strip()
            desc = line[12:82].strip()
            amount_str = line[82:96].strip()

            txn_date = datetime.strptime(date_str, "%m/%d/%Y").date()
            amount = Decimal(amount_str.replace(",", ""))

            transactions.append(
                Transaction(
                    date=txn_date,
                    description=desc,
                    amount=amount,
                    account=account_name,
                )
            )

        except Exception:
            # Hard fail later if needed; skip malformed lines for now
            continue

    return transactions
