from budget.models.envelope import Envelope


def overspent(envelopes: dict[str, Envelope]) -> dict[str, Envelope]:
    return {
        name: env
        for name, env in envelopes.items()
        if env.balance < 0
    }
