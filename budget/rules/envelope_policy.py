from budget.models.transaction import Transaction, TxnType
from budget.models.envelope import Envelope
from budget.rules.envelopes import spend


# Temporary static mapping (policy, not rules)
from budget.config.envelope_map import ENVELOPE_MAP


def choose_envelope(txn: Transaction) -> str:
    desc = txn.description.upper()

    for key, env in ENVELOPE_MAP.items():
        if key in desc:
            return env

    return "Discretionary"


def apply_transaction_to_envelopes(
    txn: Transaction,
    envelopes: dict[str, Envelope],
):
    """
    Apply a transaction to envelopes.

    Rules:
    - Only SPEND transactions affect envelopes
    - Negative amount -> spending (reduces envelope)
    - Positive amount -> refund (adds back to envelope)
    """

    if txn.txn_type != TxnType.SPEND:
        return

    env = choose_envelope(txn)

    # Normal spend
    if txn.amount < 0:
        spend(envelopes, env, txn.amount)
        return

    # Refund / reversal
    if txn.amount > 0:
        envelopes[env].balance += txn.amount
        return
