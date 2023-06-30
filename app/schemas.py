from pydantic import BaseModel, EmailStr, constr, PositiveInt, validator
from datetime import datetime, date


class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str

class User(BaseModel):
    id:int
    username:str
    email:EmailStr
    created_on:datetime
    class Config:
        orm_mode=True


class BookCreate(BaseModel):
    title:str
    author:str
    description:str
    price:int
    publisher:str
    language:str
    genre:str
    book_image:str
    in_stock:bool
    published_date: date

class BookUpdate(BaseModel):
    title:str
    author:str
    description:str
    price:int
    publisher:str
    language:str
    genre:str
    book_image:str
    in_stock:bool

class Book(BookCreate):
    id:int
    user_id:int
    user:User
    class Config:
        orm_mode=True

class ReviewCreate(BaseModel):
    text:constr(max_length=500)
    rating:PositiveInt

    @validator('rating')
    def validate_rating(cls, v):
        if v>5:
            raise ValueError("Rating should be out of 5")
        return v


class Review(ReviewCreate):
    user_id:int
    user:User
    class Config:
        orm_mode=True


class Login(BaseModel):
    username:EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None

