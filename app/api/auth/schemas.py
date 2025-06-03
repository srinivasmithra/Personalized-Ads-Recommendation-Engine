from pydantic import BaseModel
from typing import List


class UserSignup(BaseModel):
    username: str
    password: str
    age: int
    gender: str
    region: str
    interests: List[str]
    search_history: List[str]


class UserLogin(BaseModel):
    username: str
    password: str
