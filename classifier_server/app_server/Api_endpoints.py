from classifier_server.controller import Controller
from fastapi import APIRouter, HTTPException

router = APIRouter()
controller = Controller()

@router.get("/")
def status() -> dict:
    """
    Returns a basic health check to confirm the server is running.
    """
    return {"status": "working"}

@router.get("/get_features_and_unique_values")
def get_features_and_unique_values():
    """
    Retrieves the list of features and their unique values
    from the current model or dataset.
    """
    try:
        return controller.get_features_and_unique_values()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sync_model_from_remote")
def sync_model_from_remote():
    """
    Syncs the trained model from the main server to the classifier server.
    """
    try:
        controller.sync_model_from_remote()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to sync model: {str(e)}")

@router.post("/predict")
def classification(selected_params_and_values: dict[str, str]) -> dict:
    """
    Predicts a class label using the Naive Bayes model
    based on the input feature values.
    """
    try:
        return {"prediction": controller.classify(selected_params_and_values)}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")
