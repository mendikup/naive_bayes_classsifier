from enum import unique

import  pandas as pd
class Extract:
    """
    Extracts structural metadata from DataFrame.
    """

    @staticmethod
    def extract_parameters_and_their_values(df):
        """
        For each label (column name in the original table), collects the list of unique values.

        :param df: DataFrame.
        :return: Dictionary of {feature: [unique values]}.
        """
        features_and_unique_values={}
        for column in df.columns[:-1]:
            unique_value_list=df[column].unique()
            features_and_unique_values[column]=unique_value_list
        return features_and_unique_values

    @staticmethod
    def extract_columns_list(df):
        """
        Returns list of all column names in the DataFrame.
        """
        return list(df.columns)[:-1]

