from fastapi import APIRouter
from typing import Dict, List, Any
from pydantic import BaseModel
from services.Controller import Controller

class DropColumnsRequest(BaseModel):
    columns_to_delete: List[str]

router = APIRouter()
controller = Controller()

@router.get("/")
def health() -> dict:
    """
    Basic server health check endpoint.
    """
    return {"status": "ok"}

@router.get("/get_list_of_files")
def get_files_list() -> dict:
    """
    Returns a list of available CSV files.
    """
    list_of_files = controller.get_list_files()
    return {"list_of_files": list_of_files}

@router.get("/load_data/{chosen_file}")
def load_data(chosen_file: str) -> dict:
    """
    Loads the selected CSV file into memory.
    """
    controller.load_and_store_data(chosen_file)
    return {"status": "success"}

@router.get("/get_list_of_columns")
def get_list_of_columns() -> dict:
    """
    Returns a list of column names in the loaded dataset.
    """
    list_of_columns = controller.get_list_of_columns_names()
    return {"list_of_columns": list_of_columns}

@router.post("/drop_requested_columns")
def drop_requested_columns(data: DropColumnsRequest) -> dict:
    """
    Drops the specified columns from the dataset.
    """
    columns_to_drop = data.columns_to_delete
    controller.drop_columns(columns_to_drop)
    return {"status": "success"}

@router.get("/get_features_and_unique_values")
def get_features_and_unique_values() -> dict:
    """
    Returns features and their possible unique values, before training.
    """
    return controller.get_features_and_unique_values()

@router.get("/clean_df_and_train_model")
def clean_df_and_train_model() -> dict:
    """
    Cleans the data, trains the Naive Bayes model, and returns its accuracy.
    """
    controller.prepare_data_for_training()
    accuracy = controller.train_model()
    return {"accuracy": accuracy}

@router.post("/predict")
def predict(features_and_values: Dict[str, Any]) -> dict:
    """
    Predicts the class based on input feature values using the trained model.
    """
    predict = controller.classify(features_and_values)
    return {"predict": predict}
