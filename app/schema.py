from datetime import datetime
from pydantic import BaseModel

# 📦 Request body schema (validation + deserialization)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  

class PostCreate(PostBase):
    pass 

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True