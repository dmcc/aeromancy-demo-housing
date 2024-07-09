"""Encapsulate logic for working with our dataset."""

import pandas as pd
from sklearn.model_selection import train_test_split

TARGET_FEATURE = "MedHouseVal"
INPUT_FEATURES = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]


def get_dataset_split(
    dataset: pd.DataFrame,
    train: bool = True,
) -> tuple[pd.DataFrame, pd.Series]:
    """Obtain the train or test split of a dataset.

    This helps ensure that we use our dataset in a consistent way and don't
    accidentally test on train.
    """
    train_dataset, test_dataset = train_test_split(dataset, random_state=7)
    dataset = train_dataset if train else test_dataset
    return (dataset[INPUT_FEATURES], dataset[TARGET_FEATURE])
