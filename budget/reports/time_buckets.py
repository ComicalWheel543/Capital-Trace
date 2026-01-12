from collections import defaultdict
from decimal import Decimal
from datetime import date

from budget.models.transaction import Transaction, TxnType
from budget.rules.envelope_policy import choose_envelope


def bucketed_burn_rates(
    txns: list[Transaction],
    bucket_days: int,
) -> dict[str, Decimal]:
    """
    Calculate average burn per time bucket (e.g. 7-day, 14-day).
    """

    by_env = defaultdict(list)

    for t in txns:
        if t.txn_type != TxnType.SPEND or t.amount >= 0:
            continue

        env = choose_envelope(t)
        by_env[env].append(t)

    rates = {}

    for env, env_txns in by_env.items():
        dates = [t.date for t in env_txns]
        if not dates:
            continue

        span_days = max(1, (max(dates) - min(dates)).days + 1)
        buckets = max(1, span_days // bucket_days)

        total = sum(abs(t.amount) for t in env_txns)
        rates[env] = (total / Decimal(buckets)).quantize(Decimal("0.01"))

    return rates
