from budget.models.transaction import Transaction
from budget.config.envelope_map import ENVELOPE_MAP


def choose_envelope(txn: Transaction) -> str:
    """
    Determine which envelope a transaction belongs to
    based on description matching.

    This function is PURE:
    - no side effects
    - no envelope mutation
    """

    desc = txn.description.upper()

    for key, env in ENVELOPE_MAP.items():
        if key in desc:
            return env

    # Fallback for unmapped discretionary spend
    return "Discretionary_Misc"
