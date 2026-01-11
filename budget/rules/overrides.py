from budget.models.transaction import Transaction
from budget.config.overrides import OVERRIDES


def apply_overrides(txn: Transaction) -> Transaction:
    for key, forced_type in OVERRIDES.items():
        if key.upper() in txn.description.upper():
            txn.txn_type = forced_type
            txn.override = True
            return txn
    return txn
