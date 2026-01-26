from fastapi import FastAPI
from database import engine
import models
from sqlalchemy.orm import Session
from fastapi import Depends
from database import SessionLocal
from models import User
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()
#CHECKING FASTAPI SETUP
# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is running"}


# @app.get("/hello")
# def say_hello():
#     return {"message": "Hello from FastAPI!"}

#CHECKING FASTAPI WITH SQLITE SETUP
# def read_root():
#     return {"message": "FastAPI with SQLite is running"}

#CREATE DATABASE TABLES
# Create database tables
models.Base.metadata.create_all(bind=engine)


#POST TO CREATE A USER
# Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str

#UPDATING FIRST NAME AND LAST NAME
class UpdateFirstName(BaseModel):
    first_name: str

class UpdateLastName(BaseModel):
    last_name: str


#To connect to database and verify setup
@app.get("/")


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }

#GET METHOD---RETRIEVE A USER
@app.get("/users/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }

#PUT METHOD---UPDATE FIRST NAME
@app.put("/users/{username}/first-name")
def update_first_name(
    username: str,
    data: UpdateFirstName,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.first_name = data.first_name
    db.commit()

    return {"message": "First name updated successfully"}

#PUT METHOD---UPDATE LAST NAME
@app.put("/users/{username}/last-name")
def update_last_name(
    username: str,
    data: UpdateLastName,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.last_name = data.last_name
    db.commit()

    return {"message": "Last name updated successfully"}
