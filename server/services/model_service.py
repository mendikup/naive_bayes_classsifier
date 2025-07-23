from sklearn.model_selection import train_test_split
from utils.convert_numpy_types import convert_numpy_object_to_numbers
from core. naive_bayes_trainer import Naive_bayesian_trainer
from core.classifier import Classifier
from tests.test_accuracy import Tester

class Model_service:

    @staticmethod
    def train_model(storage):
        train_df, test_df = train_test_split(storage.raw_data, test_size=0.3)
        storage.model = Naive_bayesian_trainer.train_model(train_df)
        storage.accuracy =Tester.check_accuracy_percentage(storage.model , test_df)
        return storage.accuracy

    @staticmethod
    def get_features_and_unique_values(storage):
        if storage.params_and_values:
            features_and_unique_values = convert_numpy_object_to_numbers(storage.params_and_values)
            return {"exists":True,"features_and_unique_values":features_and_unique_values}
        else:
            return {"exists":False}

    @staticmethod
    def classify(storage,features_and_unique_values):
        return {Classifier.get_the_most_probability_predict(storage.model,features_and_unique_values)}
