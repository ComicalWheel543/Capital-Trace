from budget.models.transaction import Transaction
from budget.config.overrides import OVERRIDES


def apply_overrides(transactions) -> list[Transaction]:
    """
    Apply manual overrides to transactions.

    Accepts:
    - list[Transaction]
    - list[list[Transaction]]
    - mixed lists

    Enforces: only Transaction objects are processed.
    """

    flattened: list[Transaction] = []

    for item in transactions:
        if isinstance(item, list):
            for sub in item:
                if isinstance(sub, Transaction):
                    flattened.append(sub)
        elif isinstance(item, Transaction):
            flattened.append(item)
        # everything else is ignored

    for txn in flattened:
        for key, override_type in OVERRIDES.items():
            if key.upper() in txn.description.upper():
                txn.override = True
                txn.txn_type = override_type
                break

    return flattened
