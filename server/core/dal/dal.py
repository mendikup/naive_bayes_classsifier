import pandas as pd
import os



class Dal:


    @staticmethod
    def load_data(file):
        path=f"data/{file}"
        df=pd.read_csv(path)
        return df

    @staticmethod
    def get_list_of_files():
        return os.listdir("data")


