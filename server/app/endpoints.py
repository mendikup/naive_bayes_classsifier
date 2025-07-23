from fastapi import APIRouter
from services .data_srvicse import DataService
from typing import Dict, List, Any
from storage import Storage
from services.model_service import Model_service

router = APIRouter()
storage = Storage()

@router.get("/")
def hello() -> dict:
    return {"status": "good morning"}

@router.get("/get_list_of_files")
def get_files_list() -> dict:
    list_of_files = DataService.get_list_files()
    return {"list_of_files":list_of_files}

@router.get("/load_data/{chosen_file}")
def load_data(chosen_file:str) -> dict:
    DataService.load_and_store_data(chosen_file, storage)
    return {"status":"success"}

@router.get("/get_list_of_columns")
def get_list_of_columns() ->dict:
    list_of_columns = DataService.get_list_of_columns_names(storage.raw_data)
    return {"list_of_columns":list_of_columns}

@router.post("/drop_requested_columns")
def drop_requested_columns(data :Dict[str, Any]) ->dict:
    columns_to_drop = data["columns_to_delete"]
    DataService.drop_columns(storage, columns_to_drop)
    return {"status": "success"}

@router.get("/get_features_and_unique_values")
def get_features_and_unique_values() ->dict:
    return Model_service.get_features_and_unique_values(storage)

@router.get("/raw_df_handler")
def raw_df_handler() -> dict :
    DataService.prepare_data_for_training(storage)
    accuracy = Model_service.train_model(storage)
    return {"accuracy": accuracy}

@router.post("/predict")
def predict(features_and_values: Dict[str, Any]) -> dict:
    predict = Model_service.classify(storage,features_and_values)
    return {"predict": predict}