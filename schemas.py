from pydantic import BaseModel
from datetime import datetime,date


class Restaurant(BaseModel):
    id:int
    name:str
    place:str
    class Config:
        orm_mode=True

class Menus(BaseModel):
    id:int
    menu_item:str
    price:int
    date:date
    resto_id:int
    class Config:
        orm_mode=True

class User(BaseModel):
    id: int
    name:str
    email:str
    password:str
    position:str
    class Config:
        orm_mode=True

class Voting(BaseModel):
    id:int
    vote:int
    menu_id:int
    user_id:int
    date:date
    class Config:
        orm_mode=True

class LogIn(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None