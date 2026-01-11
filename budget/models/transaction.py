from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class Transaction:
    date: date
    description: str
    amount: Decimal
    account: str          # "checking", "savings", "credit"
    category: str | None = None
