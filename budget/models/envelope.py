from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Envelope:
    name: str
    balance: Decimal
