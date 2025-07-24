from core.dal.dal import Dal
from utils.extract import Extract
from utils.cleaner import Cleaner
from utils.convert_numpy_types import convert_numpy_object_to_numbers

class DataService:

    # @staticmethod
    # def get_list_files():
    #     return Dal.get_list_of_files()

    # @staticmethod
    # def load_and_store_data(file_name,storage):
    #     df = Dal.load_data(file_name)
    #     storage.raw_data = df

    # @staticmethod
    # def get_list_of_columns_names(df):
    #     return Extract.extract_columns_list(df)


    @staticmethod
    def drop_columns(storage,columns):
        storage.raw_data = Cleaner.drop_requested_columns(storage.raw_data ,columns)


    @staticmethod
    def get_features_and_unique_values(storage):
        features_and_unique_values = Extract.extract_parameters_and_their_values(storage.params_and_values)
        return features_and_unique_values

    # @staticmethod
    # def prepare_data_for_training(storage) :
    #     storage.raw_data = Cleaner.ensure_there_is_no_nan(storage.raw_data)
    #     storage.params_and_values = convert_numpy_object_to_numbers(Extract.extract_parameters_and_their_values(storage.raw_data))



