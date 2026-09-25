"""Run aggregate assurance metrics for the controlled matrix."""

import json

from dara_dt.experiments.matrix_metrics import run_matrix_metrics


def main() -> None:
    """Execute matrix metrics and print machine-readable JSON."""

    result = run_matrix_metrics()

    output = {
        "experiment": "DARA-DT aggregate assurance metrics",
        "condition_count": result.condition_count,
        "policies": {},
    }

    for item in result.policies:
        metrics = item.metrics

        output["policies"][item.policy] = {
            "true_interventions": metrics.true_interventions,
            "false_interventions": metrics.false_interventions,
            "missed_interventions": metrics.missed_interventions,
            "correct_non_interventions": (
                metrics.correct_non_interventions
            ),
            "precision": metrics.precision,
            "recall": metrics.recall,
            "false_intervention_rate": (
                metrics.false_intervention_rate
            ),
            "missed_intervention_rate": (
                metrics.missed_intervention_rate
            ),
            "accuracy": metrics.accuracy,
        }

    print(
        json.dumps(
            output,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
