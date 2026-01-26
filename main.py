from fastapi import FastAPI
from database import engine
import models

app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is running"}


# @app.get("/hello")
# def say_hello():
#     return {"message": "Hello from FastAPI!"}

# Create database tables
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI with SQLite is running"}