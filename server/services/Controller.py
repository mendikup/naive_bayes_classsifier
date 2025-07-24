from core.dal.dal import Dal
from utils.convert_numpy_types import convert_numpy_object_to_numbers
from utils.extract import Extract
from utils.cleaner import Cleaner
from sklearn.model_selection import train_test_split
from core.naive_bayes_trainer import Naive_bayesian_trainer
from tests.test_accuracy import Tester
from core.classifier import Classifier


class Controller:
    def __init__(self):
        self.model = None
        self.accuracy = None
        self.params_and_values = None
        self.raw_data = None

    @staticmethod
    def get_list_files()-> list:
        return Dal.get_list_of_files()

    def load_and_store_data(self,file_name):
        df = Dal.load_data(file_name)
        self.raw_data = df

    def prepare_data_for_training(self) :
        self.raw_data = Cleaner.ensure_there_is_no_nan(self.raw_data)
        self.params_and_values = (convert_numpy_object_to_numbers
                                  (Extract.extract_parameters_and_their_values(self.raw_data)))
        print(self.params_and_values)

    def train_model(self):
        df_to_train, test_df = train_test_split(self.raw_data, test_size=0.3)
        self.model = Naive_bayesian_trainer.train_model(df_to_train)
        self.accuracy = Tester.check_accuracy_percentage(self.model, test_df)
        return self.accuracy

    def get_list_of_columns_names(self):
        print(self.raw_data)
        return Extract.extract_columns_list(self.raw_data)

    def drop_columns(self ,columns):
        self.raw_data = Cleaner.drop_requested_columns(self.raw_data ,columns)

    def get_features_and_unique_values(self):
        if self.params_and_values:
            features_and_unique_values = convert_numpy_object_to_numbers(self.params_and_values)
            return {"exists":True,"features_and_unique_values":features_and_unique_values}
        else:
            return {"exists":False}

    def classify(self,features_and_unique_values):
        return {Classifier.get_the_most_probability_predict(self.model,features_and_unique_values)}










