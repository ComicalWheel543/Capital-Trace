from collections import defaultdict
from decimal import Decimal
from datetime import date

from budget.models.transaction import Transaction, TxnType
from budget.rules.envelope_policy import choose_envelope


def monthly_burn_rates(
    txns: list[Transaction],
) -> dict[str, Decimal]:
    """
    Calculate average monthly burn rate per envelope
    based on historical SPEND transactions.
    """

    by_envelope = defaultdict(list)

    for t in txns:
        if t.txn_type != TxnType.SPEND:
            continue

        if t.amount >= 0:
            continue  # refunds do not contribute to burn

        env = choose_envelope(t)
        by_envelope[env].append(t)

    rates: dict[str, Decimal] = {}

    for env, env_txns in by_envelope.items():
        if not env_txns:
            continue

        # Determine span of history
        dates = [t.date for t in env_txns]
        months = max(1, months_between(min(dates), max(dates)))

        total_spend = sum(abs(t.amount) for t in env_txns)
        rates[env] = (total_spend / Decimal(months)).quantize(Decimal("0.01"))

    return rates


def months_between(start: date, end: date) -> int:
    return (end.year - start.year) * 12 + (end.month - start.month) + 1
