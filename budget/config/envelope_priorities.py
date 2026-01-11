from decimal import Decimal

# Ordered list: highest priority first
# target envelope, desired funding amount
ENVELOPE_PRIORITIES = [
    ("Rent", Decimal("1200.00")),
    ("Utilities", Decimal("250.00")),
    ("Insurance", Decimal("300.00")),
    ("Groceries", Decimal("400.00")),
    ("Discretionary", Decimal("200.00")),
]
