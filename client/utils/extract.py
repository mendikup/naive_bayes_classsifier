from enum import unique

import  pandas as pd
class Extract:
    """
    Extracts structural metadata from DataFrame.
    """

    @staticmethod
    def extract_parameters_and_their_values(df):
        """
          For each column, collects the list of unique values.

          :param df: DataFrame.
          :return: Dictionary of {column: [unique values]}.
          """
        suggestions={}
        for column in df.columns[:-1]:
            unique_value_list=df[column].unique()
            suggestions[column]=unique_value_list
        return suggestions

    @staticmethod
    def extract_columns_list(df):
        """
        Returns list of all column names in the DataFrame.
        """
        return list(df.columns)

