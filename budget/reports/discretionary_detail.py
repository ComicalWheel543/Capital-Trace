from decimal import Decimal
from collections import defaultdict

from budget.models.transaction import Transaction, TxnType
from budget.models.credit_transaction import CreditTransaction
from budget.rules.envelope_policy import choose_envelope


def discretionary_breakdown(transactions):
    """
    Group discretionary spending by envelope and merchant.

    Supports:
    - cash Transactions (TxnType.SPEND, envelope via policy)
    - credit CreditTransaction (amount > 0, envelope stored)

    Returns:
    dict[envelope][merchant] = total
    """

    breakdown = defaultdict(lambda: defaultdict(Decimal))

    for t in transactions:
        # -------------------------
        # CASH TRANSACTIONS
        # -------------------------
        if isinstance(t, Transaction):
            if t.txn_type != TxnType.SPEND or t.amount >= 0:
                continue

            envelope = choose_envelope(t)
            merchant = t.description
            amount = abs(t.amount)

        # -------------------------
        # CREDIT TRANSACTIONS
        # -------------------------
        elif isinstance(t, CreditTransaction):
            if t.amount <= 0:
                continue  # ignore refunds

            envelope = t.envelope
            merchant = t.description
            amount = t.amount

        else:
            continue

        # Only discretionary envelopes
        if not envelope.startswith("Discretionary"):
            continue

        breakdown[envelope][merchant] += amount

    return breakdown
