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

def cash_summary(transactions: list[Transaction]) -> dict[str, Decimal]:
    """
    Return per-account cash totals and merged total.
    """
    totals: dict[str, Decimal] = {}
    merged = Decimal("0.00")

    for txn in transactions:
        acct = txn.account
        totals.setdefault(acct, Decimal("0.00"))
        totals[acct] += txn.amount
        merged += txn.amount

    totals["Total"] = merged
    return totals
