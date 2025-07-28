from utils.convert_numpy_types import convert_numpy_object_to_numbers
import requests
from app_models.classifier import Classifier


class Controller:
    """
    Controller that handles prediction using a remote-trained Naive Bayes model.
    Synchronizes the model from an external FastAPI service.
    """

    def __init__(self):
        """
        Initializes the controller with placeholders for model, accuracy, and features.
        """
        self.trained_model = None
        self.accuracy = None
        self.params_and_values = None

    def get_features_and_unique_values(self):
        """
        Returns the features and their possible values that were synced from the remote model.

        :return: A dictionary with 'exists' flag and the feature dictionary if available.
        """
        if self.params_and_values:
            features_and_unique_values = convert_numpy_object_to_numbers(self.params_and_values)
            return {
                "exists": True,
                "features_and_unique_values": features_and_unique_values
            }
        else:
            return {"exists": False}

    def sync_model_from_remote(self):
        """
        Sends an HTTP request to a remote FastAPI server to retrieve the latest trained model.
        Updates the local state with the received model, features, and accuracy.

        """
        try:
            # Use this for local development:
            response = requests.get("http://127.0.0.1:8000/get_latest_model")
            # Use this for Docker networking:
            # response = requests.get("http://my_server:8000/get_latest_model")

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
        """
        Predicts the class based on input features using the synced model.

        :param selected_features_and_values: Dictionary of {feature: value}
        :return: Predicted class
        """
        return Classifier.get_the_most_probability_predict(
            self.trained_model,
            selected_features_and_values
        )
