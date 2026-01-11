import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from budget.models.transaction import Transaction


def load_bofa_csv(path: Path, account_name: str) -> list[Transaction]:
    """
    Load a Bank of America CSV and return normalized Transaction objects.
    """
    transactions: list[Transaction] = []

    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # BOFA typically uses MM/DD/YYYY
            txn_date = datetime.strptime(row["Date"], "%m/%d/%Y").date()
            description = row["Description"].strip()
            amount = Decimal(row["Amount"])

            transactions.append(
                Transaction(
                    date=txn_date,
                    description=description,
                    amount=amount,
                    account=account_name,
                )
            )

    return transactions
