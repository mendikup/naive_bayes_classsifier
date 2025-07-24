from fastapi import APIRouter
from typing import Dict, List, Any
from storage import Storage


from services.Controller import Controller

router = APIRouter()
controller = Controller()
storage = Storage()

@router.get("/")
def hello() -> dict:
    return {"status": "good morning"}

@router.get("/get_list_of_files")
def get_files_list() -> dict:
    list_of_files = controller.get_list_files()
    return {"list_of_files":list_of_files}

@router.get("/load_data/{chosen_file}")
def load_data(chosen_file:str) -> dict:
    controller.load_and_store_data(chosen_file)
    return {"status":"success"}

@router.get("/get_list_of_columns")
def get_list_of_columns() ->dict:
    list_of_columns = controller.get_list_of_columns_names()
    return {"list_of_columns":list_of_columns}

@router.post("/drop_requested_columns")
def drop_requested_columns(data :Dict[str, Any]) ->dict:
    columns_to_drop = data["columns_to_delete"]
    controller.drop_columns( columns_to_drop)
    return {"status": "success"}

@router.get("/get_features_and_unique_values")
def get_features_and_unique_values() ->dict:
    return controller.get_features_and_unique_values()

@router.get("/raw_df_handler")
def raw_df_handler() -> dict :
    controller.prepare_data_for_training()
    accuracy = controller.train_model()
    return {"accuracy": accuracy}

@router.post("/predict")
def predict(features_and_values: Dict[str, Any]) -> dict:
    predict = controller.classify(features_and_values)
    return {"predict": predict}