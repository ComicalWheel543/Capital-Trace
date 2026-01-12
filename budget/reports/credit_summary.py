from decimal import Decimal
from budget.models.credit_transaction import CreditTransaction


def credit_balance(transactions: list[CreditTransaction]) -> Decimal:
    return sum(txn.amount for txn in transactions)


def credit_spend_by_envelope(transactions: list[CreditTransaction]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}
    for txn in transactions:
        totals.setdefault(txn.envelope, Decimal("0.00"))
        totals[txn.envelope] += txn.amount
    return totals
