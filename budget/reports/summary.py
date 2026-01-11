from decimal import Decimal
from budget.models.transaction import Transaction


def total_balance(transactions: list[Transaction]) -> Decimal:
    """
    Compute merged balance across all accounts.
    """
    balance = Decimal("0.00")

    for txn in transactions:
        balance += txn.amount

    return balance
