from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    name: str = Field(...,min_length=1,max_length=100)
    description: Optional[str]= Field(None, max_length=500)
    status: bool = False