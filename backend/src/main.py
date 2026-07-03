from fastapi import FastAPI
import os

MY_PROJECT = os.environ.get("MY_PROJECT")
API_KEY = os.environ.get("API_KEY")

app= FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World FastAPI",
            "MY_PROJECT": MY_PROJECT,
            "API_KEY": API_KEY}