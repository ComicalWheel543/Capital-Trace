from decimal import Decimal
from copy import deepcopy


def apply_discretionary_cut(
    burn_rates: dict[str, Decimal],
    percent_cut: Decimal,
) -> dict[str, Decimal]:
    """
    Return new burn rates with discretionary reduced by X%.

    percent_cut = 25 means reduce by 25%
    """

    if percent_cut < 0 or percent_cut > 100:
        raise ValueError("percent_cut must be between 0 and 100")

    adjusted = deepcopy(burn_rates)

    if "Discretionary" in adjusted:
        factor = (Decimal("100") - percent_cut) / Decimal("100")
        adjusted["Discretionary"] = (
            adjusted["Discretionary"] * factor
        ).quantize(Decimal("0.01"))

    return adjusted
