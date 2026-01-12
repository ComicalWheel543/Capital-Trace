from decimal import Decimal

ENVELOPE_PRIORITIES = [
    ("Rent", Decimal("1200.00")),
    ("Utilities", Decimal("200.00")),
    ("Groceries", Decimal("250.00")),

    # Discretionary (explicit, capped by allocation)
    ("Discretionary_FoodOut", Decimal("150.00")),
    ("Discretionary_Alcohol", Decimal("75.00")),
    ("Discretionary_Transport", Decimal("100.00")),
    ("Discretionary_Misc", Decimal("50.00")),
]
