from collections import defaultdict
from budget.models.transaction import Transaction, TxnType


def audit_unclassified(txns: list[Transaction]) -> list[Transaction]:
    return [t for t in txns if t.txn_type is None]


def audit_ignored(txns: list[Transaction]) -> list[Transaction]:
    return [t for t in txns if t.txn_type == TxnType.IGNORED]


def audit_overrides(txns: list[Transaction]) -> list[Transaction]:
    return [t for t in txns if t.override]


def audit_by_type(txns: list[Transaction]) -> dict[TxnType, list[Transaction]]:
    buckets = defaultdict(list)
    for t in txns:
        buckets[t.txn_type].append(t)
    return buckets


def top_spend(txns: list[Transaction], limit: int = 10) -> list[Transaction]:
    spends = [t for t in txns if t.txn_type == TxnType.SPEND]
    return sorted(spends, key=lambda t: abs(t.amount), reverse=True)[:limit]
