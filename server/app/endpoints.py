import traceback
from fastapi import APIRouter
from core.classifier import Classifier
from core.dal.dal import Dal
import pandas as pd
from core.naive_bayes_trainer import Naive_bayesian_trainer
from utils.convert_numpy_types import convert_numpy_object_to_numbers
from typing import Dict, List, Any
from tests.test_accuracy import Tester

router = APIRouter()

@router.get("/")
def hello() -> dict:
    return {"status": "good morning"}


@router.get("/get_list_of_files")
def get_files_list() -> dict:
    return {"list_of_files":Dal.get_list_of_files()}


@router.get("/load_data/{chosen_file}")
def load_data(chosen_file:str) -> dict:
    df = Dal.load_data(chosen_file)
    return {"data":df.to_dict(orient="records")}


@router.post("/train_model")
def  train_df(data: List[Dict[str, Any]]) -> dict:
    df = pd.DataFrame(data)
    statistic = Naive_bayesian_trainer.train_model(df)
    statistic = convert_numpy_object_to_numbers(statistic)
    return statistic

@router.post("/check_accuracy_rate")
def check_accuracy(data: Dict[str, Any]) -> dict:
    try:
        trained_model = data["trained_model"]
        test_df = pd.DataFrame(data["test_df"])
        accuracy = Tester.check_accuracy_percentage(trained_model, test_df)
        return {"accuracy": accuracy}
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@router.post("/predict")
def predict(data: Dict[str, Any]) -> dict:
    """Return a prediction from a trained model."""
    trained_model = data["trained_model"]
    params = data["params"]
    prediction = Classifier.get_the_most_probability_predict(trained_model, params)
    return {"prediction": prediction}
