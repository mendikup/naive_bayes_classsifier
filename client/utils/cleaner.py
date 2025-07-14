import pandas as pd

class Cleaner:
    """
    Provides data cleaning functions.
    """
    @staticmethod
    def ensure_there_is_no_nan(df):
        """
            Cleans the DataFrame by dropping rows or filling in missing values.

            :param df: DataFrame possibly containing NaN.
            :return: Cleaned DataFrame.
            """
        df=Cleaner.drop_columns_with_nan_above_threshold(df, threshold=0.6)
        df= Cleaner.drop_empty_rows(df)
        return df

    @staticmethod
    def drop_empty_rows(df):
        return  df.dropna(axis=0).copy()

    @staticmethod
    def drop_columns_with_nan_above_threshold(df, threshold=0.6):
        num_of_rows = len(df.index)
        columns_to_drop = []
        for column in df.columns:
            num_of_nans = df[column].isna().sum()
            percentage_of_nans = num_of_nans / num_of_rows
            if percentage_of_nans > threshold:
                columns_to_drop.append(column)
        df.drop(columns=columns_to_drop).copy()
        return df

    @staticmethod
    def drop_requested_columns(df, requested_columns):
        """
           Removes selected columns from the DataFrame.

           :param df: DataFrame.
           :param requested_columns: List of column names to drop.
           """
        df.drop(columns=requested_columns).copy()
        return df