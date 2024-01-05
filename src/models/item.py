from pydantic import BaseModel, Field
from typing import Optional, List
from sqlmodel import SQLModel, Field,create_engine, Session, select,Relationship
from fastapi import FastAPI,HTTPException,Query, Depends

class ItemBase(SQLModel):
    name: str = Field(...,min_length=1,max_length=100)
    description: Optional[str]= Field(None, max_length=500)
    status: bool = False

    list_id: Optional[int] = Field(default=None, foreign_key="todolist.id")


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    todolist: Optional['ToDoList'] = Relationship(back_populates="items")

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

class ItemUpdate(SQLModel):
    name: Optional[str] = Field(None,min_length=1,max_length=100)
    description: Optional[str]= Field(None, max_length=500)
    status: Optional[bool] = False
    list_id: Optional[int] = None

class ItemWithListToDoList(ItemRead):
    todolist: Optional['ToDoList'] = None
    
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session 

@app.post("/item/", response_model=ItemRead)
def create_item(
    *,
    session:Session = Depends(get_session),
    item: ItemCreate):
    with Session(engine) as session:
        db_item = Item.model_validate(item)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    
@app.get("/items/", response_model=list[ItemRead])
def read_items(
    *,
    session:Session = Depends(get_session),
    offset: int = 0, 
    limit: int = Query(default=100, le=100)):
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")
    return items
    
@app.get("/item/{item_id}", response_model=ItemRead)
def read_item(
    *,
    session:Session = Depends(get_session),
    item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
    
@app.patch("/item/{item_id}", response_model=ItemRead)
def update_item(
    *,
    session:Session = Depends(get_session),
    item_id: int, item: ItemUpdate):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
    
@app.delete("/item/{item_id}")
def delete_item(
    *,
    session:Session = Depends(get_session),
    item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
    



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

class ToDoListWithItems(ToDoListRead):
    items: List[ItemRead] = []

@app.post("/todolist/", response_model=ToDoListRead)
def create_todolist(
    *,
    session:Session = Depends(get_session),
    todolist: ToDoListCreate):
    db_todolist = ToDoList.model_validate(todolist)
    session.add(db_todolist)
    session.commit()
    session.refresh(db_todolist)
    return db_todolist

@app.get("/todolists/", response_model=list[ToDoListRead])
def read_todolists(
    *,
    session:Session = Depends(get_session),
    offset: int = 0, 
    limit: int = Query(default=100, le=100)):
    todolists = session.exec(select(ToDoList).offset(offset).limit(limit)).all()
    if not todolists:
        raise HTTPException(status_code=404, detail="ToDoLists not found")
    return todolists

@app.get("/todolist/{todolist_id}", response_model=ToDoListRead)
def read_todolist(
    *,
    session:Session = Depends(get_session),
    todolist_id: int):
    todolist = session.get(ToDoList, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="ToDoList not found")
    return todolist

@app.patch("/todolist/{todolist_id}", response_model=ToDoListRead)
def update_todolist(
    *,
    session:Session = Depends(get_session),
    todolist_id: int, todolist: ToDoListUpdate):
    db_todolist = session.get(ToDoList, todolist_id)
    if not db_todolist:
        raise HTTPException(status_code=404, detail="ToDoList not found")
    todolist_data = todolist.model_dump(exclude_unset=True)
    for key, value in todolist_data.items():
        setattr(db_todolist, key, value)
    session.add(db_todolist)
    session.commit()
    session.refresh(db_todolist)
    return db_todolist

@app.delete("/todolist/{todolist_id}")
def delete_todolist(
    *,
    session:Session = Depends(get_session),
    todolist_id: int):
    todolist = session.get(ToDoList, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="ToDoList not found")
    session.delete(todolist)
    session.commit()
    return {"ok": True}

