from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import SQLModel, Field
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...,min_length=1,max_length=100)
    description: Optional[str]= Field(None, max_length=500)
    status: bool = False