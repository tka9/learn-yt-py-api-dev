from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: "UserOut"

    # class Config:
    #     orm_mode = True

class PostOut(BaseModel):
    Post: Post
    vote: int = 0


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(UserCreate):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, ge=0, le=1)]