from fastapi import FastAPI
from .Api_endpoints import router

app = FastAPI()

app.include_router(router)