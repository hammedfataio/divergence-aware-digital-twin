"""Executable pilot-result runner for the DARA-DT B-vs-C experiment."""

import json

from dara_dt.experiments.bc_pilot import run_bc_pilot


def generate_pilot_results() -> dict:
    """Run the B-vs-C pilot and return serialisable results."""

    pilot = run_bc_pilot()

    def condition_to_dict(condition):
        return {
            "condition": condition.condition,
            "divergence_count": condition.divergence_count,
            "outcomes": {
                "no_assurance": (
                    condition.policy_results
                    .no_assurance.outcome.value
                ),
                "global_divergence": (
                    condition.policy_results
                    .global_divergence.outcome.value
                ),
                "dara_dt": (
                    condition.policy_results
                    .dara_dt.outcome.value
                ),
            },
        }

    return {
        "experiment": "B-vs-C decision-relevance pilot",
        "condition_b": condition_to_dict(
            pilot.condition_b
        ),
        "condition_c": condition_to_dict(
            pilot.condition_c
        ),
    }


def main() -> None:
    """Execute the pilot and print its results."""

    results = generate_pilot_results()

    print(
        json.dumps(
            results,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
