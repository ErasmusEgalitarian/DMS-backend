from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8085)
