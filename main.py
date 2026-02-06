from fastapi import FastAPI
from database import engine
import models
from sqlalchemy.orm import Session
from fastapi import Depends
from database import SessionLocal
from models import User
from fastapi import HTTPException
from pydantic import BaseModel
from schemas import UserCreate
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from auth import hash_password, verify_password


app = FastAPI()

def root():
    return {"message": "Backend is running"}

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    # password: str
#OLD
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # hashed_pwd = hash_password(user.password)

    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        # password_hash=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }

# #POST: Create new account (Signup)
# @app.post("/signup")
# def signup(user: UserCreate, db: Session = Depends(get_db)):

#     existing_user = db.query(models.User).filter(
#         (models.User.username == user.username) |
#         (models.User.email == user.email)
#     ).first()

#     if existing_user:
#         raise HTTPException(status_code=400, detail="User already exists")

#     new_user = models.User(
#         username=user.username,
#         first_name=user.first_name,
#         last_name=user.last_name,
#         email=user.email,
#         password_hash=hash_password(user.password)
#     )

#     db.add(new_user)
#     db.commit()

#     return {"message": "User created successfully"}

# #POST: Sign in (existing users only)
# @app.post("/signin")
# def signin(data: UserLogin, db: Session = Depends(get_db)):

#     user = db.query(models.User).filter(
#         models.User.email == data.email
#     ).first()

#     if not user or not verify_password(data.password, user.password_hash):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     return {
#         "username": user.username,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "email": user.email
#     }


# GET METHOD---RETRIEVE A USER
# To connect to database and verify setup
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
# #GET: Profile
# @app.get("/profile/{username}")
# def get_profile(username: str, db: Session = Depends(get_db)):

#     user = db.query(models.User).filter(
#         models.User.username == username
#     ).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     return {
#         "username": user.username,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "email": user.email
#     }



#UPDATING FIRST NAME AND LAST NAME
class UpdateFirstName(BaseModel):
    first_name: str

class UpdateLastName(BaseModel):
    last_name: str

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


#DELETE METHOD---DELETE A USER
@app.delete("/users/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


# @app.delete("/delete/{username}")
# def delete_user(username: str, db: Session = Depends(get_db)):

#     user = db.query(models.User).filter(
#         models.User.username == username
#     ).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     db.delete(user)
#     db.commit()

#     return {"message": "User deleted successfully"}

