import pytest
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

def test_missing_feature_returns_prediction():
    df = _sample_df()
    model = NaiveBayesTrainer.train_model(df)
    params = {"weather": "sunny"}  # Missing 'temp'

    prediction = Classifier.get_the_most_probability_predict(model, params)
    assert prediction in ["yes", "no"]

def test_unseen_feature_value_does_not_crash():
    df = _sample_df()
    model = NaiveBayesTrainer.train_model(df)
    params = {"weather": "stormy", "temp": "hot"}  # 'stormy' not in training data

    prediction = Classifier.get_the_most_probability_predict(model, params)
    assert prediction in ["yes", "no"]

def test_empty_model_raises_exception():
    with pytest.raises(Exception):
        Classifier.get_the_most_probability_predict({}, {"weather": "sunny", "temp": "hot"})
