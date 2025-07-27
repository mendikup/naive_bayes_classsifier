from fastapi import APIRouter
from typing import Dict, List, Any
from pydantic import BaseModel
from services.api_controller import ApiController

class DropColumnsRequest(BaseModel):
    columns_to_delete: List[str]

router = APIRouter()
api_controller = ApiController()

@router.get("/")
def hello() -> dict:
    return {"status": "good morning"}

@router.get("/get_list_of_files")
def get_files_list() -> dict:
    list_of_files = api_controller.get_list_files()
    return {"list_of_files":list_of_files}

@router.get("/load_data/{chosen_file}")
def load_data(chosen_file:str) -> dict:
    api_controller.load_and_store_data(chosen_file)
    return {"status":"success"}

@router.get("/get_list_of_columns")
def get_list_of_columns() ->dict:
    list_of_columns = api_controller.get_list_of_columns_names()
    return {"list_of_columns":list_of_columns}

@router.post("/drop_requested_columns")
def drop_requested_columns(data :DropColumnsRequest) ->dict:
    columns_to_drop = data.columns_to_delete
    api_controller.drop_columns(columns_to_drop)
    return {"status": "success"}

@router.get("/get_features_and_unique_values")
def get_features_and_unique_values() ->dict:
    return api_controller.get_features_and_unique_values()

@router.get("/clean_df_and_train_model")
def raw_df_handler() -> dict :
    api_controller.prepare_data_for_training()
    accuracy = api_controller.train_model()
    return {"accuracy": accuracy}

@router.post("/predict")
def predict(features_and_values: Dict[str, Any]) -> dict:
    predict = api_controller.classify(features_and_values)
    return {"predict": predict}

@router.get("/get_latest_model")
def get_latest_model():
    return api_controller.get_latest_model()
