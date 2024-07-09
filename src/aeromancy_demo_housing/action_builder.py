"""Aeromancy `ActionBuilder` for aeromancy-demo-housing."""

from aeromancy import Action, ActionBuilder
from typing_extensions import override

from aeromancy_demo_housing.actions import (
    EvaluationAction,
    IngestHousingDataset,
    TrainLinearRegressionAction,
)


class HousingModelActionBuilder(ActionBuilder):
    """ActionBuilder for aeromancy-demo-housing."""

    def __init__(
        self,
    ):
        """Create an `ActionBuilder` for aeromancy-demo-housing."""
        # The project name is for organizational purposes and will be the
        # project name in Weights and Biases.
        ActionBuilder.__init__(self, project_name="aeromancy_demo_housing")

    @override
    def build_actions(self) -> list[Action]:
        actions = []

        ingest_action = self.add_action(actions, IngestHousingDataset(parents=[]))
        train_action = self.add_action(
            actions,
            TrainLinearRegressionAction(parents=[ingest_action]),
        )
        self.add_action(
            actions,
            EvaluationAction(
                ingest_dataset=ingest_action,
                train_model=train_action,
            ),
        )
        return actions
