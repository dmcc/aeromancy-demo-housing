"""Aeromancy `Action`s for aeromancy-demo-housing.

This provides some example actions for a simple machine learning pipeline:

1. Ingest: Store a dataset as an Aeromancy artifact.
2. Train: Train a model from the dataset. Output a serialized trained model.
3. Evaluation: Read the data and the trained model, evaluate the model on the
   dataset. Produce evaluation metrics and output the model predictions.
"""

import tempfile
from pathlib import Path

import pandas as pd
import sklearn.datasets
import skops.io
from aeromancy import Action, S3Object, Tracker
from loguru import logger
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing_extensions import override

from .dataset_utils import get_dataset_split


class IngestHousingDataset(Action):
    """Download and ingest the housing dataset."""

    job_type = "ingest-dataset"
    job_group = "model"

    @override
    def outputs(self) -> list[str]:
        return ["housing-dataset"]

    @override
    def run(self, tracker: Tracker) -> None:
        dataset = sklearn.datasets.fetch_california_housing(as_frame=True)
        logger.info("Dataset:")
        logger.info(dataset)

        # Save it in Parquet data format for convenience. (In an ideal world, we
        # might save the original as well and transform it in a later pipeline
        # stage)
        dataset_filename = Path("ingest/cal_housing_prices_data.parquet")
        dataset["frame"].to_parquet(dataset_filename)

        [dataset_artifact_name] = self.outputs()
        tracker.declare_output(
            name=dataset_artifact_name,
            local_filenames=[dataset_filename],
            s3_destination=S3Object("aeromancy-demo-housing", "datasets/"),
            artifact_type="dataset",
            strip_prefix="ingest/",
        )


class TrainLinearRegressionAction(Action):
    """Train a linear regression model to predict housing prices."""

    job_type = "train-model"
    job_group = "model"

    @override
    def outputs(self) -> list[str]:
        return ["linear-model"]

    @override
    def run(self, tracker: Tracker) -> None:
        [dataset_artifact_name], [model_artifact_name] = self.get_io()
        [dataset_path] = tracker.declare_input(dataset_artifact_name)

        logger.info("Reading dataset...")
        dataset = pd.read_parquet(dataset_path)
        input_features, target_feature = get_dataset_split(dataset, train=True)

        logger.info("Training model...")
        model = LinearRegression()
        model.fit(input_features, target_feature)
        logger.info("Model:", model.coef_, model.intercept_)

        logger.info("Saving model...")
        output_dir = Path(tempfile.mkdtemp())
        model_path = output_dir / "linear-model.skops"
        skops.io.dump(model, model_path)

        # Save the model as an Aeromancy Artifact.
        tracker.declare_output(
            name=model_artifact_name,
            local_filenames=[model_path],
            s3_destination=S3Object("aeromancy-demo-housing", "models/"),
            artifact_type="model",
            strip_prefix=model_path.parent,
        )


class EvaluationAction(Action):
    """Evaluate model predictions."""

    job_type = "eval-model"
    job_group = "model"

    def __init__(
        self,
        ingest_dataset: IngestHousingDataset,
        train_model: TrainLinearRegressionAction,
    ):
        Action.__init__(self, parents=[ingest_dataset, train_model])

    @override
    def outputs(self) -> list[str]:
        return ["model-predictions"]

    @override
    def run(self, tracker: Tracker) -> None:
        (
            [dataset_artifact_name, model_artifact_name],
            [predictions_artifact_name],
        ) = self.get_io()

        [dataset_path] = tracker.declare_input(dataset_artifact_name)
        [model_path] = tracker.declare_input(model_artifact_name)

        logger.info("Loading dataset...")
        dataset = pd.read_parquet(dataset_path)
        input_features, target_feature = get_dataset_split(dataset, train=False)

        logger.info("Loading model...")
        model = skops.io.load(model_path)

        predictions_numpy = model.predict(input_features)
        predictions = pd.DataFrame({"prediction": predictions_numpy})

        logger.info("Saving predictions...")
        output_dir = Path(tempfile.mkdtemp())
        predictions_path = output_dir / "model_predictions.parquet"
        predictions.to_parquet(predictions_path)

        metrics = {
            "mse": float(mean_squared_error(target_feature, predictions)),
            "mae": float(mean_absolute_error(target_feature, predictions)),
            "r2": r2_score(target_feature, predictions),
        }

        # Output our evaluation metrics.
        tracker.log(metrics)

        # Store our model predictions.
        tracker.declare_output(
            name=predictions_artifact_name,
            local_filenames=[predictions_path],
            s3_destination=S3Object("aeromancy-demo-housing", "predictions/"),
            artifact_type="predictions",
            strip_prefix=predictions_path.parent,
        )
