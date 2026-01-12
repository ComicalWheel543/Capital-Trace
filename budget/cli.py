import argparse
from decimal import Decimal

from budget.reports.goal_optimizer import optimize_goals
from budget.reports.projections import project_runway
from budget.scenarios.discretionary_cut import apply_discretionary_cut


def run_discretionary_scenario(
    envelopes,
    burn_rates,
    target_months,
    cut_percent,
):
    adjusted_burn = apply_discretionary_cut(
        burn_rates,
        Decimal(cut_percent),
    )

    burn_matrix = {
        env: {"adjusted": rate}
        for env, rate in adjusted_burn.items()
    }

    goals = optimize_goals(burn_matrix, target_months)
    runway = project_runway(envelopes, adjusted_burn)

    print(f"\n=== SCENARIO: Discretionary -{cut_percent}% ===")

    print("\nAdjusted Burn Rates:")
    for env, rate in adjusted_burn.items():
        print(f"{env:<15} ${rate}")

    print("\nOptimized Goals:")
    for env, goal in goals.items():
        print(f"{env:<15} ${goal}")

    print("\nRunway (Months):")
    for env, months in runway.items():
        print(f"{env:<15} {months}")


def build_parser():
    parser = argparse.ArgumentParser(description="Capital-Trace CLI")

    parser.add_argument(
        "--cut-discretionary",
        type=int,
        help="Reduce discretionary burn by X percent",
    )

    parser.add_argument(
    "--spend-summary",
    action="store_true",
    help="Show total spend by envelope",
    )

    parser.add_argument(
        "--discretionary-detail",
        action="store_true",
        help="Show discretionary spending by merchant",
    )

    return parser
