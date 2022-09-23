from typing import Union
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[EmailStr, None] = None


class UserBase(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    hashed_password: str

class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_stuff: bool