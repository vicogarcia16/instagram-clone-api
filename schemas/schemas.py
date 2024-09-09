from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)
    
class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int

class User(BaseModel):
    username: str
    model_config = ConfigDict(from_attributes=True)
    
class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
    
class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: User
    comments: List[Comment]
    model_config = ConfigDict(from_attributes=True) 

class UserAuth(BaseModel):
    id: int
    username: str
    password: str

class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int
