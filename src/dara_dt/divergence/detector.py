"""Physical–digital divergence detection for DARA-DT."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Divergence:
    """Represents a detected physical–digital state discrepancy."""

    entity_type: str
    entity_id: str
    variable: str
    physical_value: Any
    twin_value: Any

    @property
    def path(self) -> str:
        """Return the canonical path of the divergent variable."""
        return f"{self.entity_type}.{self.entity_id}.{self.variable}"


class DivergenceDetector:
    """Detect discrepancies between physical and Digital Twin states."""

    def detect(
        self,
        physical_state: dict[str, Any],
        twin_state: dict[str, Any],
    ) -> list[Divergence]:
        """Return all detected physical–digital divergences."""
        divergences: list[Divergence] = []

        for entity_type in ("vehicles", "orders"):
            physical_entities = physical_state.get(entity_type, {})
            twin_entities = twin_state.get(entity_type, {})

            shared_ids = physical_entities.keys() & twin_entities.keys()

            for entity_id in shared_ids:
                physical_entity = physical_entities[entity_id]
                twin_entity = twin_entities[entity_id]

                shared_variables = (
                    physical_entity.keys() & twin_entity.keys()
                )

                for variable in shared_variables:
                    physical_value = physical_entity[variable]
                    twin_value = twin_entity[variable]

                    if physical_value != twin_value:
                        divergences.append(
                            Divergence(
                                entity_type=entity_type,
                                entity_id=entity_id,
                                variable=variable,
                                physical_value=physical_value,
                                twin_value=twin_value,
                            )
                        )

        return divergences
