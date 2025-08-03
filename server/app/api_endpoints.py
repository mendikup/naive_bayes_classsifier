from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
from pydantic import BaseModel
from services.api_controller import ApiController

class DropColumnsRequest(BaseModel):
    columns_to_delete: List[str]

router = APIRouter()
api_controller = ApiController()

@router.get("/")
def health() -> dict:
    return {"status": "ok"}

@router.get("/get_list_of_files")
def get_files_list() -> dict:
    """
    Returns a list of available CSV files for selection.
    """
    try:
        list_of_files = api_controller.get_list_files()
        return {"list_of_files": list_of_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting file list: {str(e)}")

@router.get("/load_data/{chosen_file}")
def load_data(chosen_file: str) -> dict:
    """
    Loads the selected CSV file and stores it in memory.
    """
    try:
        api_controller.load_and_store_data(chosen_file)
        return {"status": "success"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

@router.get("/get_list_of_columns")
def get_list_of_columns() -> dict:
    """
    Returns a list of column names from the currently loaded dataset.
    """
    try:
        list_of_columns = api_controller.get_list_of_columns_names()
        return {"list_of_columns": list_of_columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving columns: {str(e)}")

@router.post("/drop_requested_columns")
def drop_requested_columns(data: DropColumnsRequest) -> dict:
    """
    Drops the specified columns from the current dataset.
    """
    try:
        columns_to_drop = data.columns_to_delete
        api_controller.drop_columns(columns_to_drop)
        return {"status": "success"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid columns: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to drop columns: {str(e)}")

@router.get("/get_features_and_unique_values")
def get_features_and_unique_values() -> dict:
    """
    Returns the features and their possible unique values (before training).
    """
    try:
        return api_controller.get_features_and_unique_values()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get features: {str(e)}")

@router.get("/clean_df_and_train_model")
def clean_df_and_train_model() -> dict:
    """
    Cleans the dataset, trains the Naive Bayes model, and returns the accuracy.
    """
    try:
        api_controller.prepare_data_for_training()
        accuracy = api_controller.train_model()
        return {"accuracy": accuracy}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@router.post("/predict")
def predict(features_and_values: Dict[str, Any]) -> dict:
    """
    Predicts the class based on provided feature values using the trained model.
    """
    try:
        prediction = api_controller.classify(features_and_values)
        return {"predict": prediction}
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/get_latest_model")
def get_latest_model():
    """
    Returns the latest trained model, its accuracy, and the extracted features.
    """
    try:
        return api_controller.get_latest_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve model: {str(e)}")
