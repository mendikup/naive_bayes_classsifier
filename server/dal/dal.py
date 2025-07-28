
import pandas as pd
import os



class Dal:
    """
    Handles data access operations like reading CSV files or URLs.
    """

    @staticmethod
    def load_data(file):
        # path=f"data/{file}"
        path = os.path.join("data" ,file)
        if not os.path.exists(path):
             raise FileNotFoundError (f"file not found: {path}")

        try:
            df = pd.read_csv(path)
            return df
        except Exception as e:
            raise ValueError (f"Failed to load CSV: {e}")

    @staticmethod
    def get_list_of_files():
        return os.listdir("data")

