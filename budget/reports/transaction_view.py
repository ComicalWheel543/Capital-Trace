from budget.models.transaction import Transaction, TxnType
from budget.rules.envelope_policy import choose_envelope


def transactions_for_envelope(
    txns: list[Transaction],
    envelope: str,
) -> list[Transaction]:
    """
    Return all transactions contributing to an envelope.
    """

    return [
        t for t in txns
        if t.txn_type == TxnType.SPEND
        and t.amount < 0
        and choose_envelope(t) == envelope
    ]
