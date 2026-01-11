from decimal import Decimal
from budget.models.envelope import Envelope


def project_runway(
    envelopes: dict[str, Envelope],
    burn_rates: dict[str, Decimal],
) -> dict[str, Decimal]:
    """
    Returns how many months each envelope can survive
    at its current burn rate.
    """

    runway: dict[str, Decimal] = {}

    for name, env in envelopes.items():
        if name == "Unallocated":
            continue

        burn = burn_rates.get(name, Decimal("0.00"))

        if burn <= 0:
            runway[name] = Decimal("Infinity")
            continue

        runway[name] = (env.balance / burn).quantize(Decimal("0.01"))

    return runway
