from decimal import Decimal
from budget.models.envelope import Envelope


def simulate_spend(
    envelopes: dict[str, Envelope],
    envelope_name: str,
    amount: Decimal,
    caps: dict[str, Decimal],
    burn_rates: dict[str, Decimal],
) -> list[str]:
    """
    Simulate a spend and return warnings.
    Does NOT mutate envelopes.
    """

    warnings: list[str] = []

    if amount <= 0:
        raise ValueError("Simulated spend amount must be positive")

    if envelope_name not in envelopes:
        raise KeyError(f"Envelope '{envelope_name}' does not exist")

    env = envelopes[envelope_name]
    projected_balance = env.balance - amount

    cap = caps.get(envelope_name)
    burn = burn_rates.get(envelope_name, Decimal("0.00"))

    # 1. Spending beyond allocated envelope
    if projected_balance < 0:
        warnings.append(
            f"Spend exceeds allocated balance by ${abs(projected_balance):.2f}"
        )

    # 2. Cap violation (behavioral)
    if cap is not None and burn > cap:
        warnings.append(
            f"Envelope already over monthly cap (${burn} > ${cap})"
        )

    # 3. Runway impact
    if burn > 0:
        projected_months = projected_balance / burn
        if projected_months < Decimal("1.00"):
            warnings.append(
                f"Projected runway < 1 month after spend ({projected_months:.2f})"
            )

    return warnings
