# FastAPI User Management API

This project is a simple API built using **FastAPI** and **SQLite**.  
It demonstrates basic CRUD (Create, Read, Update, Delete) operations on a User and is tested using **Postman**.

---

## Features
- Create a user
- Get user details using username
- Update user first name
- Update user last name
- Delete a user

---

## Tech Stack
- Python
- FastAPI
- SQLite
- SQLAlchemy
- Postman

---

## Project Setup

1. Create Virtual Environment
2. Activate Virtual Environment
3. Install Dependencies
4. Run the Application(uvicorn main:app --reload)
Server runs at: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs
5.  Create User-POST /
6. Get User by Username-GET /users/{username}
7. Update First Name-PUT /users/{username}/first-name
8. Update Last Name-PUT /users/{username}/last-name
9. Delete User-DELETE /users/{username}

### Testing Using Postman

Open Postman
Create a new request
Select the appropriate HTTP method
Use the endpoint URL
Send JSON data for POST and PUT requests
Verify responses