from collections import defaultdict
from decimal import Decimal

from budget.models.transaction import Transaction, TxnType
from budget.rules.envelope_policy import choose_envelope


def spend_by_envelope(
    txns: list[Transaction],
) -> dict[str, Decimal]:
    """
    Total spend per envelope (historical).
    """

    totals = defaultdict(Decimal)

    for t in txns:
        if t.txn_type != TxnType.SPEND:
            continue

        if t.amount >= 0:
            continue  # ignore refunds

        env = choose_envelope(t)
        totals[env] += abs(t.amount)

    return dict(totals)
