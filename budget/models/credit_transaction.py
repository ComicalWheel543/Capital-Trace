from dataclasses import dataclass
from decimal import Decimal
from datetime import date


@dataclass
class CreditTransaction:
    date: date
    description: str
    amount: Decimal   # POSITIVE = charge, NEGATIVE = refund
    envelope: str
    statement_month: str
