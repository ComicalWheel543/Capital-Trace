from decimal import Decimal


def credit_float_warning(
    starting_balance: Decimal,
    ending_balance: Decimal,
):
    delta = ending_balance - starting_balance

    if delta > 0:
        print(f"\n⚠ CREDIT BALANCE GREW: +${delta:.2f}")
    elif delta < 0:
        print(f"\n✓ CREDIT BALANCE REDUCED: ${-delta:.2f}")
    else:
        print("\n✓ CREDIT BALANCE STABLE")
