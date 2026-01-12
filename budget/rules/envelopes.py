from decimal import Decimal
from budget.models.envelope import Envelope


def initial_envelopes(total_cash: Decimal) -> dict[str, Envelope]:
    """
    Create the initial envelope set.
    All cash starts in Unallocated.
    """

    return {
        "Unallocated": Envelope("Unallocated", total_cash),

        # Core envelopes
        "Rent": Envelope("Rent", Decimal("0.00")),
        "Utilities": Envelope("Utilities", Decimal("0.00")),
        "Groceries": Envelope("Groceries", Decimal("0.00")),
        "Insurance": Envelope("Insurance", Decimal("0.00")),

        # Discretionary
        "Discretionary_FoodOut": Envelope("Discretionary_FoodOut", Decimal("0.00")),
        "Discretionary_Alcohol": Envelope("Discretionary_Alcohol", Decimal("0.00")),
        "Discretionary_Transport": Envelope("Discretionary_Transport", Decimal("0.00")),
        "Discretionary_Cash": Envelope("Discretionary_Cash", Decimal("0.00")),
        "Discretionary_Subscriptions": Envelope("Discretionary_Subscriptions", Decimal("0.00")),
        "Discretionary_Misc": Envelope("Discretionary_Misc", Decimal("0.00")),
    }


def allocate_by_priority(envelopes, priorities):
    for name, amount in priorities:
        if envelopes["Unallocated"].balance <= 0:
            break

        allocation = min(amount, envelopes["Unallocated"].balance)
        envelopes["Unallocated"].balance -= allocation
        envelopes[name].balance += allocation
