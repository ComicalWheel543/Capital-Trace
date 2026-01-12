from collections import defaultdict
from decimal import Decimal

from budget.models.transaction import TxnType
from budget.rules.envelope_policy import choose_envelope


def discretionary_breakdown(txns):
    """
    Return discretionary spending grouped by sub-envelope,
    then by merchant.
    """

    breakdown = defaultdict(lambda: defaultdict(Decimal))

    for t in txns:
        if t.txn_type != TxnType.SPEND or t.amount >= 0:
            continue

        env = choose_envelope(t)
        if not env.startswith("Discretionary_"):
            continue

        merchant = t.description[:40]
        breakdown[env][merchant] += abs(t.amount)

    return breakdown
