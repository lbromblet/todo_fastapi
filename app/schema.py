from pydantic import BaseModel
from typing import List, Optional


class Todo(BaseModel):
    title: str
    complete: bool

    class Config:
        orm_mode = True


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    complete: Optional[bool] = None
    
    class Config:
        orm_mode = True