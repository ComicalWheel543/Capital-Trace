from pathlib import Path

from budget.ingest.txt_import import load_bofa_txt
from budget.rules.transfers import remove_internal_transfers
from budget.rules.overrides import apply_overrides
from budget.rules.classify import classify_transaction
from budget.rules.envelopes import initial_envelopes, allocate_by_priority
from budget.reports.summary import total_balance
from budget.reports.burn_rates import monthly_burn_rates
from budget.reports.projections import project_runway
from budget.reports.caps import cap_status
from budget.reports.warnings import envelope_warnings
from budget.config.envelope_priorities import ENVELOPE_PRIORITIES
from budget.config.envelope_caps import ENVELOPE_CAPS


def main():
    # ----------------------------
    # Load statements
    # ----------------------------
    checking_txns, checking_start = load_bofa_txt(
        Path("data/checking.txt"),
        "checking",
    )

    savings_txns, savings_start = load_bofa_txt(
        Path("data/savings.txt"),
        "savings",
    )

    # ----------------------------
    # Current cash state
    # ----------------------------
    checking_end = checking_start + total_balance(checking_txns)
    savings_end = savings_start + total_balance(savings_txns)
    total_cash = checking_end + savings_end

    # ----------------------------
    # Merge + classify history
    # ----------------------------
    all_txns = checking_txns + savings_txns
    merged_txns = remove_internal_transfers(all_txns)

    txns = [apply_overrides(t) for t in merged_txns]
    txns = [classify_transaction(t) for t in txns]

    # ----------------------------
    # Envelopes (current plan)
    # ----------------------------
    envelopes = initial_envelopes(total_cash)
    allocate_by_priority(envelopes, ENVELOPE_PRIORITIES)

    # ----------------------------
    # Projections
    # ----------------------------
    burn_rates = monthly_burn_rates(txns)
    runway = project_runway(envelopes, burn_rates)
    caps = cap_status(envelopes, ENVELOPE_CAPS)
    warnings = envelope_warnings(runway, burn_rates, ENVELOPE_CAPS)

    # ----------------------------
    # Reporting
    # ----------------------------
    print("\n=== CASH ===")
    print(f"Checking: ${checking_end}")
    print(f"Savings:  ${savings_end}")
    print(f"Total:    ${total_cash}")

    print("\n=== ENVELOPES ===")
    for env in envelopes.values():
        print(f"{env.name:<15} ${env.balance}")

    print("\n=== CAPS ===")
    for name, info in caps.items():
        print(
            f"{name:<15} "
            f"Allocated ${info['allocated']} / "
            f"Cap ${info['cap']} "
            f"(Remaining ${info['remaining']})"
        )

    print("\n=== RUNWAY (MONTHS) ===")
    for env, months in runway.items():
        print(f"{env:<15} {months}")

    if warnings:
        print("\n⚠ WARNINGS ⚠")
        for env, msgs in warnings.items():
            for msg in msgs:
                print(f"{env:<15} {msg}")

    # Invariant check
    envelope_sum = sum(env.balance for env in envelopes.values())
    if envelope_sum != total_cash:
        raise RuntimeError(
            f"Invariant violated: envelopes ${envelope_sum} != cash ${total_cash}"
        )


if __name__ == "__main__":
    main()
