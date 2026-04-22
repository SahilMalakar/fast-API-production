from pydantic import BaseModel

# 📦 Request body schema (validation + deserialization)
class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True  