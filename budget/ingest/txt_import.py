from datetime import datetime
from decimal import Decimal
from pathlib import Path

from budget.models.transaction import Transaction


def load_bofa_txt(path: Path, account_name: str) -> tuple[list[Transaction], Decimal]:
    """
    Parse a Bank of America TXT statement (fixed-width / column-aligned format).

    Returns:
        (transactions, starting_balance)
    """

    transactions: list[Transaction] = []
    starting_balance: Decimal | None = None

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

        # Capture beginning balance (do NOT treat as a transaction)
        if "Beginning balance" in line:
            # Balance is right-aligned at end of line
            try:
                starting_balance = Decimal(line.rsplit(maxsplit=1)[-1].replace(",", ""))
            except Exception as e:
                raise RuntimeError(f"Failed to parse starting balance:\n{line}") from e
            continue

        # ---- TRANSACTION PARSING ----
        try:
            # Split from the right:
            # [date + description] [amount] [running balance]
            parts = line.rsplit(maxsplit=2)

            if len(parts) < 3:
                raise ValueError("Line does not have expected 3 right-aligned columns")

            amount_str = parts[-2]
            left = parts[0]

            # Date is always first 10 chars (MM/DD/YYYY)
            date_str = left[:10]
            description = left[10:].strip()

            txn_date = datetime.strptime(date_str, "%m/%d/%Y").date()
            amount = Decimal(amount_str.replace(",", ""))

            transactions.append(
                Transaction(
                    date=txn_date,
                    description=description,
                    amount=amount,
                    account=account_name,
                )
            )

        except Exception as e:
            raise RuntimeError(f"Failed to parse transaction line:\n{line}") from e

    if starting_balance is None:
        raise RuntimeError("Starting balance not found in statement")

    return transactions, starting_balance
