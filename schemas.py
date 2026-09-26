from pydantic import BaseModel
from typing import Optional, Any

class BookBase(BaseModel):
    title: str
    author: str
    category: str
    quantity: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Optional[Any] = None