from pydantic import BaseModel
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool
    rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class UpdatePost(PostBase):
    published: bool

class Post(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True
    

class Author(BaseModel):
    first_name: str
    name: str