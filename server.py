from fastapi import FastAPI
import uvicorn
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from src import service

app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=['*'],
        )
    ]
)


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/measurements")
def get_measurements(user_id: str):
    return service.get_measurements(user_id)


@app.get("/waste-pickers")
def get_waste_pickers():
    return service.get_waste_pickers()


@app.get("/waste-pickers/{waste_picker_id}")
def get_waste_picker(waste_picker_id: str):
    return service.get_waste_picker(waste_picker_id)


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8085, reload=True)
