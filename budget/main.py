from decimal import Decimal
from pathlib import Path
import argparse

# =========================
# INGEST
# =========================
from budget.ingest.txt_import import load_bofa_txt
from budget.ingest.credit_csv import load_credit_csv

# =========================
# RULES
# =========================
from budget.rules.classify import classify_transactions
from budget.rules.overrides import apply_overrides

# =========================
# MODELS / ENVELOPES
# =========================
from budget.models.envelope import Envelope
from budget.rules.envelopes import initial_envelopes

# =========================
# REPORTS
# =========================
from budget.reports.summary import cash_summary
from budget.reports.burn_rates import monthly_burn_rates
from budget.reports.discretionary_detail import discretionary_breakdown
from budget.reports.credit_summary import (
    credit_balance,
    credit_spend_by_envelope,
)
from budget.reports.credit_warnings import credit_float_warning

# =========================
# PLANNING (PHASE 5.2)
# =========================
from budget.config.income import INCOME_CONFIG
from budget.config.targets import ENVELOPE_TARGETS
from budget.config.priorities import (
    ESSENTIAL_ENVELOPES,
    DISCRETIONARY_ENVELOPES,
)
from budget.planning.requirements import compute_required_funding
from budget.planning.allocation import allocate_income


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--discretionary-detail",
        action="store_true",
        help="Show discretionary breakdown by sub-envelope",
    )
    args = parser.parse_args()

    # =========================
    # CASH INGEST
    # =========================
    cash_txns = []
    cash_txns += load_bofa_txt(Path("data/checking.txt"), "Checking")
    cash_txns += load_bofa_txt(Path("data/savings.txt"), "Savings")

    # =========================
    # CLASSIFY + OVERRIDES
    # =========================
    cash_txns = classify_transactions(cash_txns)
    cash_txns = apply_overrides(cash_txns)

    # =========================
    # CREDIT INGEST (STATEMENT)
    # =========================
    credit_txns = load_credit_csv(
        Path("data/credit.csv"),
        statement_month="2026-01",
    )

    # =========================
    # CASH SUMMARY
    # =========================
    cash = cash_summary(cash_txns)

    print("\n=== CASH ===")
    print(f"Checking: ${cash['Checking']:.2f}")
    print(f"Savings:  ${cash['Savings']:.2f}")
    print(f"Total:    ${cash['Total']:.2f}")

    # =========================
    # CREDIT SUMMARY
    # =========================
    credit_total = credit_balance(credit_txns)

    print("\n=== CREDIT CARD ===")
    print(f"Statement Balance: ${credit_total:.2f}")

    # =========================
    # DISCRETIONARY DETAIL (OPTIONAL)
    # =========================
    if args.discretionary_detail:
        breakdown = discretionary_breakdown(cash_txns + credit_txns)

        print("\n=== DISCRETIONARY BREAKDOWN ===")
        for env in sorted(breakdown.keys()):
            merchants = breakdown[env]
            total = sum(merchants.values())

            print(f"\n[{env}] Total: ${total:.2f}")
            for merchant, amount in sorted(
                merchants.items(),
                key=lambda x: x[1],
                reverse=True,
            ):
                print(f"  {merchant:<40} ${amount:.2f}")

        return

    # =========================
    # ENVELOPES (CURRENT STATE)
    # =========================
    envelopes: dict[str, Envelope] = initial_envelopes(Decimal(cash["Total"]))

    print("\n=== CURRENT ENVELOPES ===")
    for env in envelopes.values():
        print(f"{env.name:<22} ${env.balance:.2f}")

    # =========================
    # BURN RATES
    # =========================
    burn_rates = monthly_burn_rates(cash_txns)

    # ADD CREDIT SPEND INTO BURN
    credit_burn = credit_spend_by_envelope(credit_txns)
    for env, amt in credit_burn.items():
        burn_rates[env] = burn_rates.get(env, Decimal("0.00")) + amt

    print("\n=== BURN RATES (MONTHLY) ===")
    for env, burn in sorted(burn_rates.items()):
        print(f"{env:<28} ${burn:.2f}")

    # =========================
    # PHASE 5.2 — INCOME-AWARE PLANNING
    # =========================
    monthly_income = INCOME_CONFIG["monthly_amount"]

    required = compute_required_funding(burn_rates, ENVELOPE_TARGETS)
    allocation = allocate_income(monthly_income, required)

    print("\n=== INCOME ASSUMPTIONS ===")
    print(f"Monthly Income: ${monthly_income:.2f}")

    print("\n=== MONTHLY FUNDING REQUIREMENTS (HYBRID) ===")
    for env, amount in required.items():
        print(f"{env:<28} ${amount:.2f}")

    print("\n=== INCOME ALLOCATION (PRIORITY) ===")

    for env in ESSENTIAL_ENVELOPES:
        data = allocation.get(env)
        if not data:
            continue

        status = "✓" if data["shortfall"] == 0 else "⚠"
        print(
            f"{env:<28} "
            f"Funded ${data['funded']:.2f} / ${data['required']:.2f} {status}"
        )

    disc = allocation["DISCRETIONARY_BLOCK"]

    print("\n--- DISCRETIONARY BLOCK ---")
    print(f"Required: ${disc['required']:.2f}")
    print(f"Funded:   ${disc['funded']:.2f}")

    if disc["shortfall"] > 0:
        print(f"⚠ Shortfall: ${disc['shortfall']:.2f}")

        print("\nDiscretionary Drivers:")
        total_required = sum(
            required.get(env, Decimal("0.00"))
            for env in DISCRETIONARY_ENVELOPES
        )

        for env in DISCRETIONARY_ENVELOPES:
            amt = required.get(env, Decimal("0.00"))
            if amt > 0:
                pct = (amt / total_required) * 100
                print(f"  {env:<28} ${amt:.2f} ({pct:.1f}%)")

    # =========================
    # CREDIT FLOAT AWARENESS
    # =========================
    credit_float_warning(
        starting_balance=Decimal("0.00"),
        ending_balance=credit_total,
    )


if __name__ == "__main__":
    main()
