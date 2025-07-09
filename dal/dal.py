import pandas as pd
import os


class Dal:

    def __init__(self):
        self.files_list=os.listdir("../data")



    def load_data(self ,path):
        df=pd.read_csv(path)

        return df
