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

# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is running"}


# @app.get("/hello")
# def say_hello():
#     return {"message": "Hello from FastAPI!"}

# Create database tables
models.Base.metadata.create_all(bind=engine)

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


def read_root():
    return {"message": "FastAPI with SQLite is running"}