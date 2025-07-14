from fastapi import APIRouter
from pydantic import BaseModel
from server.core.dal.dal import Dal
import pandas as pd
from server.core.naive_bayes_trainer import Naive_bayesian_trainer
from server.utils.convert_numpy_types import convert_numpy_object_to_numbers
from typing import Dict, List, Any

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
# def  train_df(data:list[dict[str,any]]) -> dict:
def  train_df(data: List[Dict[str, Any]]) -> dict:
    df = pd.DataFrame(data)
    statistic = Naive_bayesian_trainer.train_model(df)
    statistic = convert_numpy_object_to_numbers(statistic)
    return statistic

