from decimal import Decimal

def compute_required_funding(
    burn_rates: dict[str, Decimal],
    targets: dict[str, Decimal],
) -> dict[str, Decimal]:
    required = {}

    for env, burn in burn_rates.items():
        target = targets.get(env, Decimal("0.00"))
        required[env] = max(burn, target)

    return required
