from classifer_server.controller import Controller
from fastapi import APIRouter

router = APIRouter()
controller = Controller()

@router.get("/")
def status() -> dict:
    return {"status": "working"}

@router.get("/get_features_and_unique_values")
def get_features_and_unique_values():
    return controller.get_features_and_unique_values()

@router.get("/update_storage")
def update_storage():
    controller.update_storage()
    return {"status": "success"}

@router.post("/classify")
def classification(selected_params_and_values: dict[str, str]) -> dict:
    return {"prediction":controller.classify(selected_params_and_values)}
