from fastapi import FastAPI,Depends
from sqlmodel import SQLModel, create_engine, Session, select,Field
from todo_server import settings
from contextlib import asynccontextmanager
from typing import Union,Optional,Annotated


#create class
class Todo(SQLModel,table=True):
    id:int = Field( default=None , primary_key=True)
    title:str
#create engine

connection_str=str(settings.DATABASE_URL).replace("postgresql","postgresql+psycopg")

engine=create_engine(connection_str)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("creating tables...")
    create_db_tables()
    yield

app:FastAPI=FastAPI(lifespan=lifespan)

#create session for dependancy injection
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def index():
    return {"message":"Hello World"}

@app.post("/todo/", response_model=Todo)
def create_todo(todo: Todo, session:Annotated[Session,Depends(get_session)]):
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
#for update todo
@app.put("/todo/{id}", response_model=Todo)
def update_todo(id:int, todo:Todo, session:Annotated[Session, Depends(get_session)]):
    todo_to_update=session.get(Todo, id)
    todo_to_update.title=todo.title
    session.commit()
    session.refresh(todo_to_update)
    return todo_to_update    
#for delete todo
@app.delete("/todo/{id}", response_model=Todo)
def delete_todo(id:int, session:Annotated[Session, Depends(get_session)]):
    todo_to_delete=session.get(Todo, id)
    session.delete(todo_to_delete)
    session.commit()
    return todo_to_delete
# get specific todo against todo ID
@app.get("/todo/{id}", response_model=Todo)
def get_todo(id:int, session:Annotated[Session, Depends(get_session)]):
    todo=session.get(Todo, id)
    return todo