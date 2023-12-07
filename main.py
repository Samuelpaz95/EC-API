from fastapi import FastAPI
from src import init_app

app = init_app(FastAPI())


@app.get("/")
def read_main():
    return {"message": "Hello World"}
