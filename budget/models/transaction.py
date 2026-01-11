from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


class TxnType(str, Enum):
    INCOME = "income"
    SPEND = "spend"
    TRANSFER = "transfer"
    PAYMENT = "payment"
    IGNORED = "ignored"


@dataclass
class Transaction:
    date: date
    description: str
    amount: Decimal
    account: str

    txn_type: TxnType | None = None
    override: bool = False
