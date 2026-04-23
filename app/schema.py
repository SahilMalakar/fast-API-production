from datetime import datetime
from pydantic import BaseModel, EmailStr,Field
from typing import Annotated




class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True
    
class AuthResponse(BaseModel):
    message: str
    user: UserResponse
    class Config:
        from_attributes = True






# 📦 Request body schema (validation + deserialization)
class VoteBase(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True


class PostResponseWithVotes(BaseModel):
    post: PostResponse
    votes: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
    email: str | None = None