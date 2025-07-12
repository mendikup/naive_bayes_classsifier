from enum import unique

import  pandas as pd
class Extract_keys:

    @staticmethod
    def extract(df):
        suggestions={}
        for column in df.columns[:-1]:
            unique_value_list=df[column].uniqe
            suggestions[column]=unique_value_list
        return

