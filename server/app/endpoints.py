from fastapi import APIRouter
from pydantic import BaseModel
from server.core.dal.dal import Dal

router = APIRouter()


class Something(BaseModel):
    name: str
    value: int

@router.get("/")
def health():
    return {"message": "working"}


@router.post("/post")
def post(something: Something):
    print(something)
    return something

@router.get("/get_list_of_files")
def get_files_list():
    return {"list_of_files":Dal.get_list_of_files()}


@router.get("/load_data/{chosen_file}")
def load_data(chosen_file):
    df = Dal.load_data(chosen_file)
    return {"data":df.to_dict(orient="records")}
