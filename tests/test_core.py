
import pandas as pd
from server.core.naive_bayes_trainer import NaiveBayesTrainer
from server.core.classifier import Classifier


def _sample_df():
    return pd.DataFrame(
        {
            "weather": ["sunny", "sunny", "rainy", "overcast"],
            "temp": ["hot", "cool", "hot", "mild"],
            "play": ["no", "yes", "yes", "yes"],
        }
    )


def test_train_model_basic_probabilities():
    df = _sample_df()
    model = NaiveBayesTrainer.train_model(df)

    assert model["sum"]["total_cases"] == 4
    assert model["no"]["weather"]["sunny"] == 0.5


def test_classifier_prediction():
    df = _sample_df()
    model = NaiveBayesTrainer.train_model(df)
    params = {"weather": "overcast", "temp": "mild"}
    prediction = Classifier.get_the_most_probability_predict(model, params)

    assert prediction == "yes"

