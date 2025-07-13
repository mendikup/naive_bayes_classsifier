from enum import unique

import  pandas as pd
class Extract:

    @staticmethod
    def extract_parameters_and_their_values(df):
        suggestions={}
        for column in df.columns[:-1]:
            unique_value_list=df[column].unique()
            suggestions[column]=unique_value_list
        return suggestions

    @staticmethod
    def extract_columns_list(df):
        return list(df.columns)

