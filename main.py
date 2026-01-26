from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}


@app.get("/hello")
def say_hello():
    return {"message": "Hello from FastAPI!"}
