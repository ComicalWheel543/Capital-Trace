from decimal import Decimal


def optimize_goals(
    burn_rates: dict[str, dict[str, Decimal]],
    target_months: Decimal,
) -> dict[str, Decimal]:
    """
    Determine recommended envelope balances to survive target months,
    using the WORST burn rate across buckets.
    """

    goals = {}

    for env, rates in burn_rates.items():
        worst_rate = max(rates.values(), default=Decimal("0.00"))
        goals[env] = (worst_rate * target_months).quantize(Decimal("0.01"))

    return goals
