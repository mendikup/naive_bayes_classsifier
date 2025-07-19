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
        df = df.copy()
        trained_by = df.columns[-1]
        # df.sort_values(trained_by, inplace=True)

        column_trained_by = df[trained_by]
        # Remove the target column from the model DataFrame to ensure it's not mistakenly used as a feature during training
        df_without_target_value_column=df.drop( columns=[trained_by])
        # initialize the dictionary model with a nested  dictionary called sum to save the calculations to use theme in the end
        bayes_model = {"sum": {"total_cases": len(df_without_target_value_column.index)}}


        for target_value in column_trained_by.unique():
            #  for each option count the number of times it appears in the class column (we will need it for calculations in the end
            bayes_model['sum'][target_value] = (df[trained_by] == target_value).sum()

            bayes_model[target_value] = {}
            for feature in df.columns:
                bayes_model[target_value][feature] = {}
                for unique_key in df[feature].unique():

                    # Creates a boolean mask for rows where the feature equals unique_key
                    # and the target column equals target_value
                    mask = ((df[feature] == unique_key) & (df[trained_by] == target_value))
                    match_count = mask.sum() + 1  # Includes Laplace
                    num_unique_feature_values = df[feature].nunique()
                    total_target_value_count = bayes_model['sum'][ target_value] + num_unique_feature_values  # Includes Laplace



                    bayes_model[target_value][feature][unique_key] = match_count/total_target_value_count

        return bayes_model







