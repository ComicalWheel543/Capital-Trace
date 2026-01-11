from decimal import Decimal
from budget.models.envelope import Envelope


def initial_envelopes(total_cash: Decimal) -> dict[str, Envelope]:
    """
    Create the initial envelope set.

    Rules:
    - All cash starts in Unallocated
    - All other envelopes start at 0
    """

    return {
        "Unallocated": Envelope("Unallocated", total_cash),
        "Rent": Envelope("Rent", Decimal("0.00")),
        "Utilities": Envelope("Utilities", Decimal("0.00")),
        "Groceries": Envelope("Groceries", Decimal("0.00")),
        "Insurance": Envelope("Insurance", Decimal("0.00")),
        "Discretionary": Envelope("Discretionary", Decimal("0.00")),
    }


def allocate(
    envelopes: dict[str, Envelope],
    target: str,
    amount: Decimal,
):
    """
    Move money from Unallocated into a target envelope.
    """

    if amount <= 0:
        raise ValueError("Allocation amount must be positive")

    if envelopes["Unallocated"].balance < amount:
        raise ValueError("Insufficient Unallocated funds")

    envelopes["Unallocated"].balance -= amount
    envelopes[target].balance += amount


def allocate_by_priority(
    envelopes: dict[str, Envelope],
    priorities: list[tuple[str, Decimal]],
):
    """
    Allocate money into envelopes by priority until cash runs out.

    Rules:
    - Allocates up to desired amount per envelope
    - Stops automatically when Unallocated hits zero
    - Never raises due to insufficient funds
    """

    for name, desired in priorities:
        if envelopes["Unallocated"].balance <= 0:
            break

        available = envelopes["Unallocated"].balance
        allocation = min(desired, available)

        if allocation > 0:
            envelopes["Unallocated"].balance -= allocation
            envelopes[name].balance += allocation


def spend(
    envelopes: dict[str, Envelope],
    source: str,
    amount: Decimal,
):
    """
    Apply spending to an envelope.
    Overspending is allowed and visible.
    """

    if amount >= 0:
        raise ValueError("Spend amount must be negative")

    envelopes[source].balance += amount
