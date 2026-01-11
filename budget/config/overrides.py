from budget.models.transaction import TxnType

# description substring : forced transaction type
OVERRIDES = {
    "DISCOUNT LIQ": TxnType.SPEND,
    "PAYPAL DES:TRANSFER": TxnType.TRANSFER,
    "BAL INQ": TxnType.IGNORED,
}
