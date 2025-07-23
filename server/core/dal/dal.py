import pandas as pd
import os



class Dal:
    """
    Handles data access operations like reading CSV files or URLs.
    """

    @staticmethod
    def load_data(file):
        path=f"data/{file}"
        print(path)
        # path = os.path.join("data", file)

        # print(os.path.dirname(path))
        if os.path.exists(path):
            print("tesssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        else:
            print("nooooooooooooooooooooooooooooooooooooooooooooooo")
        df = pd.read_csv(path)
        return df

    @staticmethod
    def get_list_of_files():
        return os.listdir("data")

