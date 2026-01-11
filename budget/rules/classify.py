from budget.models.transaction import Transaction, TxnType


INCOME_KEYWORDS = [
    "PAYROLL",
    "EDWARD D. JONES",
]

TRANSFER_KEYWORDS = [
    "ONLINE BANKING TRANSFER",
    "TRANSFER TO",
    "TRANSFER FROM",
]

PAYMENT_KEYWORDS = [
    "PAYMENT TO CRD",
    "CREDIT CARD PAYMENT",
    "MOBILE BANKING PAYMENT TO CRD",
]


def classify_transaction(txn: Transaction) -> Transaction:
    """
    Assign a default transaction type.
    Does NOT override manually classified transactions.
    """

    if txn.override:
        return txn

    desc = txn.description.upper()

    # Income must be money coming in
    if txn.amount > 0 and any(k in desc for k in INCOME_KEYWORDS):
        txn.txn_type = TxnType.INCOME
        return txn

    # Credit card payments are NOT spending
    if any(k in desc for k in PAYMENT_KEYWORDS):
        txn.txn_type = TxnType.PAYMENT
        return txn

    # Transfers between owned accounts
    if any(k in desc for k in TRANSFER_KEYWORDS):
        txn.txn_type = TxnType.TRANSFER
        return txn

    # Default rule: money leaving = spending
    if txn.amount < 0:
        txn.txn_type = TxnType.SPEND
        return txn

    # Anything else is noise / refunds / weird bank artifacts
    txn.txn_type = TxnType.IGNORED
    return txn
