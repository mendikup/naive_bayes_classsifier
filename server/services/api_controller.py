from core.dal.dal import Dal
from utils.convert_numpy_types import convert_numpy_object_to_numbers
from utils.extract import Extract
from utils.cleaner import Cleaner
from sklearn.model_selection import train_test_split
from core.naive_bayes_trainer import NaiveBayesTrainer
from utils.test_accuracy import Tester
from core.classifier import Classifier



class ApiController:
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
        if self.raw_data is None:
            raise ValueError("No data loaded")
        self.raw_data = Cleaner.ensure_there_is_no_nan(self.raw_data)
        self.params_and_values = (convert_numpy_object_to_numbers
                                  (Extract.extract_parameters_and_their_values(self.raw_data)))
        print(self.params_and_values)

    def train_model(self):
        if self.raw_data is None:
            raise ValueError("No data loaded")
        df_to_train, test_df = train_test_split(self.raw_data, test_size=0.3)
        self.model = NaiveBayesTrainer.train_model(df_to_train)
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
            return {"exists":True,
                    "features_and_unique_values":features_and_unique_values}
        else:
            return {"exists":False}

    def classify(self,features_and_unique_values):
        return {Classifier.get_the_most_probability_predict(self.model,features_and_unique_values)}

    def get_latest_model(self):
        if not self.model:
            return {"exists":False}
        else:
            return {"exists":True,
                    "trained_model":convert_numpy_object_to_numbers(self.model),
                    "features_and_unique_keys":convert_numpy_object_to_numbers(self.params_and_values),
                    "accuracy":self.accuracy
                    }











