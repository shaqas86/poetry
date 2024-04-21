# main.py
from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated
from todo_server import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str 


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield


app:FastAPI = FastAPI(lifespan=lifespan) 
    
def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)]):
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(Todo)).all()
        return todos














# from fastapi import FastAPI,Depends
# from sqlmodel import SQLModel, create_engine, Session, select,Field
# from todo_server import settings
# from contextlib import asynccontextmanager
# from typing import Union,Optional,Annotated


# #create class
# class Todo(SQLModel,table=True):
#     id:int = Field( default=None , primary_key=True)
#     title:str
# #create engine

# connection_str=str(settings.DATABASE_URL).replace("postgresql","postgresql+psycopg")

# engine=create_engine(connection_str)

# def create_db_tables():
#     SQLModel.metadata.create_all(engine)

# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     print("creating tables...")
#     create_db_tables()
#     yield

# app:FastAPI=FastAPI(lifespan=lifespan)

# #create session for dependancy injection
# def get_session():
#     with Session(engine) as session:
#         yield session

# @app.get("/")
# def index():
#     return {"message":"Hello World"}

# @app.post("/todo/", response_model=Todo)
# def create_todo(todo: Todo, session:Annotated[Session,Depends(get_session)]):
#         session.add(todo)
#         session.commit()
#         session.refresh(todo)
#         return todo
# #for update todo
# @app.put("/todo/{id}", response_model=Todo)
# def update_todo(id:int, todo:Todo, session:Annotated[Session, Depends(get_session)]):
#     todo_to_update=session.get(Todo, id)
#     todo_to_update.title=todo.title
#     session.commit()
#     session.refresh(todo_to_update)
#     return todo_to_update    
# #for delete todo
# @app.delete("/todo/{id}", response_model=Todo)
# def delete_todo(id:int, session:Annotated[Session, Depends(get_session)]):
#     todo_to_delete=session.get(Todo, id)
#     session.delete(todo_to_delete)
#     session.commit()
#     return todo_to_delete
# # get specific todo against todo ID
# @app.get("/todo/{id}", response_model=Todo)
# def get_todo(id:int, session:Annotated[Session, Depends(get_session)]):
#     todo=session.get(Todo, id)
#     return todo