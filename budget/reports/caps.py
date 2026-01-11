from decimal import Decimal
from budget.models.envelope import Envelope


def cap_status(
    envelopes: dict[str, Envelope],
    caps: dict[str, Decimal],
) -> dict[str, dict[str, Decimal | bool]]:
    """
    Compare envelope balances against caps.

    Returns per-envelope status:
    - cap
    - allocated
    - remaining
    - over_cap (bool)
    """

    status = {}

    for name, env in envelopes.items():
        if name == "Unallocated":
            continue

        cap = caps.get(name)

        if cap is None:
            continue

        allocated = env.balance
        remaining = cap - allocated

        status[name] = {
            "cap": cap,
            "allocated": allocated,
            "remaining": remaining,
            "over_cap": allocated > cap,
        }

    return status
