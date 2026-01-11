from decimal import Decimal
from collections import defaultdict
from budget.models.transaction import Transaction


def find_internal_transfers(transactions: list[Transaction]) -> set[int]:
    """
    Returns a set of transaction indices that are part of internal transfers.
    """
    used = set()
    amount_map = defaultdict(list)

    for idx, txn in enumerate(transactions):
        amount_map[abs(txn.amount)].append((idx, txn))

    for amount, txns in amount_map.items():
        if len(txns) < 2:
            continue

        for i in range(len(txns)):
            idx1, t1 = txns[i]
            if idx1 in used:
                continue

            for j in range(i + 1, len(txns)):
                idx2, t2 = txns[j]
                if idx2 in used:
                    continue

                # Opposite sign, different account, close in time
                if (
                    t1.amount == -t2.amount
                    and t1.account != t2.account
                    and abs((t1.date - t2.date).days) <= 3
                ):
                    used.add(idx1)
                    used.add(idx2)
                    break

    return used


def remove_internal_transfers(transactions: list[Transaction]) -> list[Transaction]:
    to_remove = find_internal_transfers(transactions)
    return [t for i, t in enumerate(transactions) if i not in to_remove]
