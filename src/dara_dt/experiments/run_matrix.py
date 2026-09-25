"""Executable results runner for the DARA-DT experimental matrix."""

import json

from dara_dt.experiments.experimental_matrix import (
    run_experimental_matrix,
)


def generate_matrix_results() -> dict:
    """Execute the experimental matrix and return serialisable results."""

    matrix = run_experimental_matrix()

    rows = []

    for row in matrix.rows:
        rows.append(
            {
                "condition": row.condition,
                "divergence_count": row.divergence_count,
                "relevant_count": row.relevant_count,
                "outcomes": {
                    "no_assurance": row.no_assurance.value,
                    "global_divergence": (
                        row.global_divergence.value
                    ),
                    "dara_dt": row.dara_dt.value,
                },
            }
        )

    return {
        "experiment": (
            "DARA-DT controlled experimental matrix"
        ),
        "condition_count": len(rows),
        "policies": [
            "no_assurance",
            "global_divergence",
            "dara_dt",
        ],
        "results": rows,
    }


def main() -> None:
    """Execute the matrix and print machine-readable results."""

    results = generate_matrix_results()

    print(
        json.dumps(
            results,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
