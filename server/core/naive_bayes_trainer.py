import pandas as pd
import numpy as np
import pprint

from pyexpat import features


class NaiveBayesTrainer:
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
        df = df.copy()
        target_col = df.columns[-1]
        features = df.columns [: -1]
        total_rows = len(df)

        # initialize the dictionary model with a nested  dictionary called sum to save the calculations to use them in the end
        bayes_model = {"sum": {"total_cases": total_rows}}

        for target_value in df[target_col] .unique():
            #  for each option count the number of times it appears in the class column (we will need it for calculations in the end
            target_value_count =(df[target_col] == target_value).sum()
            bayes_model['sum'][target_value] = target_value_count
            bayes_model[target_value] = {}
            for feature in features:
                bayes_model[target_value][feature] = {}
                for unique_key in df[feature].unique():

                    # Creates a boolean mask for rows where the feature equals unique_key
                    # and the target column equals target_value
                    count = ((df[feature] == unique_key) & (df[target_col] == target_value))
                    match_count = count.sum() + 1  # Includes Laplace
                    num_unique_feature_values = df[feature].nunique()
                    total_target_value_count = bayes_model['sum'][ target_value] + num_unique_feature_values  # Includes Laplace

                    bayes_model[target_value][feature][unique_key] = match_count/total_target_value_count

        return bayes_model







