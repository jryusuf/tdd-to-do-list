from pydantic import BaseModel, Field
from typing import Optional, List
from sqlmodel import SQLModel, Field,create_engine, Session, select, Relationship
from fastapi import FastAPI,HTTPException,Query, Depends
import src.models.item as item

class ToDoListBase(SQLModel):
    name: str = Field(...,min_length=1,max_length=100)
    description: Optional[str]= Field(None, max_length=500)

class ToDoList(ToDoListBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    items: List['Item'] = Relationship(back_populates="todolist")

class ToDoListCreate(ToDoListBase):
    pass

class ToDoListRead(ToDoListBase):
    id: int

class ToDoListUpdate(SQLModel):
    name: Optional[str] = Field(None,min_length=1,max_length=100)
    description: Optional[str]= Field(None, max_length=500)

