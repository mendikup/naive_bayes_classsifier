import pandas as pd
import numpy as np
import pprint

class Naive_bayesian_trainer:
    """
    Trains a Naive Bayes model from a given dataset.
     """


@staticmethod
def train_model(df):
    """
           Builds a Naive Bayes model (nested dict of probabilities) from training data.

           :param df: pandas DataFrame with labeled data.
           :return: Nested dict {class_label: {column_name: {value: probability}}}
           """
    # 1. Count class frequencies (prior probabilities)
    # 2. For each class and column, count value frequencies (likelihoods)
    # 3. Normalize into probabilities, apply Laplace smoothing if needed

    # Make a copy to preserve the original data (will be used for calculations)
    df_for_stats = df.copy()

    # The name of the target column (i.e., the column to be predicted)
    target_column = df.columns[-1]

    # Extract the target values (class labels) to a separate Series
    target_values = df[target_column]

    # Remove the target column from the training data to avoid using it as a feature
    df.drop(columns=[target_column], inplace=True)

    # Initialize the statistics dictionary. "sum" will hold global totals.
    statistics = {
        "sum": {
            "total_cases": len(df_for_stats.index)  # Total number of rows in the dataset
        }
    }

    # Iterate over each unique class label in the target column
    for class_label in target_values.unique():
        # Count how many times this class label appears in the dataset
        statistics["sum"][class_label] = (df_for_stats[target_column] == class_label).sum()

        # Initialize sub-dictionary for this class
        statistics[class_label] = {}

        # Iterate over each feature column
        for feature_column in df.columns:
            statistics[class_label][feature_column] = {}

            # Iterate over each unique value in the feature column
            for feature_value in df[feature_column].unique():
                # Count how many times this value appears for this class (with Laplace smoothing)
                count = ((df_for_stats[feature_column] == feature_value) &
                         (df_for_stats[target_column] == class_label)).sum()

                # Apply Laplace smoothing (+1 numerator)
                statistics[class_label][feature_column][feature_value] = (count + 1) / statistics["sum"][
                    class_label]

    return statistics
