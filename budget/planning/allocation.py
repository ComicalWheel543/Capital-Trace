from decimal import Decimal
from budget.config.priorities import (
    ESSENTIAL_ENVELOPES,
    DISCRETIONARY_ENVELOPES,
)

def allocate_income(
    monthly_income: Decimal,
    required: dict[str, Decimal],
):
    remaining = monthly_income
    results = {}

    # Essentials first
    for env in ESSENTIAL_ENVELOPES:
        need = required.get(env, Decimal("0.00"))
        funded = min(need, remaining)
        remaining -= funded

        results[env] = {
            "required": need,
            "funded": funded,
            "shortfall": need - funded,
        }

    # Discretionary as a block
    discretionary_required = sum(
        required.get(e, Decimal("0.00")) for e in DISCRETIONARY_ENVELOPES
    )

    discretionary_funded = min(discretionary_required, remaining)
    discretionary_shortfall = discretionary_required - discretionary_funded

    results["DISCRETIONARY_BLOCK"] = {
        "required": discretionary_required,
        "funded": discretionary_funded,
        "shortfall": discretionary_shortfall,
    }

    return results
