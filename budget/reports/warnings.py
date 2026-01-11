from decimal import Decimal


def envelope_warnings(
    runway: dict[str, Decimal],
    burn_rates: dict[str, Decimal],
    caps: dict[str, Decimal],
) -> dict[str, list[str]]:
    """
    Generate human-readable warnings per envelope.
    """

    warnings = {}

    for env, months in runway.items():
        env_warnings = []

        burn = burn_rates.get(env, Decimal("0.00"))
        cap = caps.get(env)

        if months != Decimal("Infinity") and months < Decimal("1.00"):
            env_warnings.append(f"Runway < 1 month ({months})")

        if cap is not None and burn > cap:
            env_warnings.append(
                f"Monthly burn ${burn} exceeds cap ${cap}"
            )

        if env_warnings:
            warnings[env] = env_warnings

    return warnings
