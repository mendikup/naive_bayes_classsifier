from core.dal.dal import Dal
from utils.convert_numpy_types import convert_numpy_object_to_numbers
from utils.extract import Extract
from utils.cleaner import Cleaner
from sklearn.model_selection import train_test_split
from core.naive_bayes_trainer import NaiveBayesTrainer
from utils.test_accuracy import Tester
from core.classifier import Classifier


class Controller:
    """
    Controls the full training and prediction process for a Naive Bayes classifier.
    Handles data loading, preprocessing, model training, accuracy checking, and prediction.
    """

    def __init__(self):
        """
        Initializes the controller with empty state.
        """
        self.trained_model = None
        self.accuracy = None
        self.params_and_values = None
        self.raw_data = None

    @staticmethod
    def get_list_files() -> list:
        """
        Returns a list of available CSV files from the DAL.
        """
        return Dal.get_list_of_files()

    def load_and_store_data(self, file_name):
        """
        Loads the data from the given file and stores it in memory.

        :param file_name: The name of the CSV file to load.
        """
        df = Dal.load_data(file_name)
        self.raw_data = df

    def prepare_data_for_training(self):
        """
        Cleans the loaded data and extracts feature names and possible values.

        :raises ValueError: If no data is loaded.
        """
        if self.raw_data is None:
            raise ValueError("No data loaded")

        self.raw_data = Cleaner.ensure_there_is_no_nan(self.raw_data)
        self.params_and_values = convert_numpy_object_to_numbers(
            Extract.extract_parameters_and_their_values(self.raw_data)
        )

    def train_model(self):
        """
        Trains the Naive Bayes model using 70% of the data, tests on 30%, and saves the results.

        :return: Accuracy percentage on the test set.
        :raises ValueError: If no data is loaded.
        """
        if self.raw_data is None:
            raise ValueError("No data loaded")

        df_to_train, test_df = train_test_split(self.raw_data, test_size=0.3)
        self.trained_model = NaiveBayesTrainer.train_model(df_to_train)
        self.accuracy = Tester.check_accuracy_percentage(self.trained_model, test_df)
        return self.accuracy

    def get_list_of_columns_names(self):
        """
        Returns the list of column names in the current dataset.
        """
        print(self.raw_data)
        return Extract.extract_columns_list(self.raw_data)

    def drop_columns(self, columns):
        """
        Drops the specified columns from the data.

        :param columns: A list of column names to drop.
        """
        self.raw_data = Cleaner.drop_requested_columns(self.raw_data, columns)

    def get_features_and_unique_values(self):
        """
        Returns the features and their unique values extracted from the dataset.

        :return: A dictionary with 'exists' flag and the actual feature dictionary if available.
        """
        if self.params_and_values:
            features_and_unique_values = convert_numpy_object_to_numbers(self.params_and_values)
            return {
                "exists": True,
                "features_and_unique_values": features_and_unique_values
            }
        else:
            return {"exists": False}

    def classify(self, features_and_unique_values):
        """
        Predicts the class for a given set of feature values using the trained model.

        :param features_and_unique_values: A dictionary of {feature: value}
        :return: A set with the predicted class label.
        """
        return {Classifier.get_the_most_probability_predict(self.trained_model, features_and_unique_values)}
