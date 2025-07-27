from utils.convert_numpy_types import convert_numpy_object_to_numbers
import requests
from app_models.classifier import Classifier


class Controller:
    def __init__(self):
        self.trained_model = None
        self.accuracy = None
        self.params_and_values = None

    def get_features_and_unique_values(self):
        if self.params_and_values:
            features_and_unique_values = convert_numpy_object_to_numbers(self.params_and_values)
            return {"exists": True,
                    "features_and_unique_values": features_and_unique_values}
        else:
            return {"exists": False}

    def sync_model_from_remote(self):
        try:
            # response = requests.get("http://my_server:8000/get_latest_model")  # for docker
            response = requests.get("http://127.0.0.1:8000/get_latest_model")
            if response.ok:
                content = response.json()
                if content['exists']:
                    features_and_unique_keys = content['features_and_unique_keys']
                    trained_model = content['trained_model']
                    accuracy = content['accuracy']

                    self.params_and_values = features_and_unique_keys
                    self.trained_model = trained_model
                    self.accuracy = accuracy
                    print("updated successfully")
        except Exception as e:
            print("There was an error with the server.")
            print(f"Error: {e}.")


    def classify(self, selected_features_and_values):
        return Classifier.get_the_most_probability_predict(self.trained_model, selected_features_and_values)