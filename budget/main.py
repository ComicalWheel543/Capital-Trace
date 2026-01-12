from pathlib import Path
from decimal import Decimal
import sys

from budget.ingest.txt_import import load_bofa_txt
from budget.rules.transfers import remove_internal_transfers
from budget.rules.overrides import apply_overrides
from budget.rules.classify import classify_transaction
from budget.rules.envelopes import initial_envelopes, allocate_by_priority

from budget.reports.summary import total_balance
from budget.reports.burn_rates import monthly_burn_rates
from budget.reports.time_buckets import bucketed_burn_rates
from budget.reports.goal_optimizer import optimize_goals
from budget.reports.projections import project_runway

from budget.scenarios.discretionary_cut import apply_discretionary_cut
from budget.cli import build_parser, run_discretionary_scenario
from budget.config.envelope_priorities import ENVELOPE_PRIORITIES


def main():
    # ----------------------------
    # CLI parsing (scenario mode)
    # ----------------------------
    parser = build_parser()
    args, _ = parser.parse_known_args()

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
    merged = remove_internal_transfers(all_txns)
    txns = [classify_transaction(apply_overrides(t)) for t in merged]

    # ----------------------------
    # Envelopes (current intent)
    # ----------------------------
    envelopes = initial_envelopes(total_cash)
    allocate_by_priority(envelopes, ENVELOPE_PRIORITIES)

    # ----------------------------
    # Burn rates
    # ----------------------------
    burn_monthly = monthly_burn_rates(txns)
    burn_weekly = bucketed_burn_rates(txns, 7)

    burn_matrix = {}
    for env in set(burn_monthly) | set(burn_weekly):
        burn_matrix[env] = {
            "monthly": burn_monthly.get(env, Decimal("0.00")),
            "weekly": burn_weekly.get(env, Decimal("0.00")) * Decimal("4"),
        }

    # ----------------------------
    # Scenario: discretionary cut
    # ----------------------------
    if args.cut_discretionary is not None:
        run_discretionary_scenario(
            envelopes=envelopes,
            burn_rates=burn_monthly,
            target_months=Decimal("2.00"),
            cut_percent=args.cut_discretionary,
        )
        return

    # ----------------------------
    # Goal optimization
    # ----------------------------
    target_months = Decimal("2.00")
    goals = optimize_goals(burn_matrix, target_months)

    # ----------------------------
    # Projections
    # ----------------------------
    runway = project_runway(envelopes, burn_monthly)

    # ----------------------------
    # Reporting
    # ----------------------------
    print("\n=== CASH ===")
    print(f"Total Cash: ${total_cash}")

    print("\n=== CURRENT ENVELOPES ===")
    for env in envelopes.values():
        print(f"{env.name:<15} ${env.balance}")

    print("\n=== OPTIMIZED GOALS (2-MONTH SURVIVAL) ===")
    for env, goal in goals.items():
        current = envelopes.get(env).balance if env in envelopes else Decimal("0.00")
        delta = goal - current
        status = "UNDER" if delta > 0 else "OVER"
        print(
            f"{env:<15} Goal ${goal} | "
            f"Current ${current} | "
            f"{status} by ${abs(delta):.2f}"
        )

    print("\n=== RUNWAY (MONTHS) ===")
    for env, months in runway.items():
        print(f"{env:<15} {months}")

    # ----------------------------
    # Invariant
    # ----------------------------
    if sum(e.balance for e in envelopes.values()) != total_cash:
        raise RuntimeError("Envelope invariant violated")


if __name__ == "__main__":
    main()
