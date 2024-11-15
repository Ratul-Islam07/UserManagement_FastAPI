from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict 

app = FastAPI()

users_db: Dict[int, dict] = {}

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None

@app.post("/users", response_model=User)
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user.dict()
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user.dict()
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}

@app.get("/users", response_model=list[User])
def get_all_users():
    return list(users_db.values())
