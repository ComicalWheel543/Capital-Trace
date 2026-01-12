from collections import defaultdict
from decimal import Decimal

from budget.models.transaction import Transaction, TxnType
from budget.rules.envelope_policy import choose_envelope


def discretionary_by_merchant(
    txns: list[Transaction],
) -> dict[str, Decimal]:
    """
    Breakdown of discretionary spending by merchant.
    """

    totals = defaultdict(Decimal)

    for t in txns:
        if t.txn_type != TxnType.SPEND or t.amount >= 0:
            continue

        if choose_envelope(t) != "Discretionary":
            continue

        merchant = t.description[:40]  # keep it readable
        totals[merchant] += abs(t.amount)

    return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))
