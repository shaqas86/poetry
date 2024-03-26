from contextlib import asynccontextmanager
from fastapi  import FastAPI
from typing import Union,Optional
from todo_api import settings
from sqlmodel import Field,Session,SQLModel,create_engine,select

class Todo(SQLModel,table=True):
    id:int =Field(default=None,primary_key=True)
    title:str =Field(index=True)

connection_string=str(settings.DATABASE_URL).replace(
    "postgresql","postgresql+psycopg")

engine=create_engine(connection_string,
                     connect_args={"sslmode":"require"},pool_recycle=300)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app :FastAPI):
    print("creating tables..")
    create_db_and_tables()
    yield

app :FastAPI= FastAPI(lifespan=lifespan)  


@app.get("/")
def read_root():
    return {"Hello": "World"}
# todo with data inseration
@app.post("/todos")
def create_todo(todo:Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
# endpoing with  path parameter
@app.get("/todos/")
def read_todos():
    with Session(engine) as session:
        todos=session.exec(select(Todo)).all()
        return todos
# endpoint with data updation
@app.put("/todos/{id}")
def update_todo(id:int,todo:Todo):
    with Session(engine) as session:
        todo_to_update=session.get(Todo,id)
        todo_to_update.title=todo.title
        session.add(todo_to_update)
        session.commit()
        session.refresh(todo_to_update)
        return todo_to_update
# delete endpoint
@app.delete("/todos/{id}")
def delete_todo(id: int,todo: Todo):
    with Session(engine) as session:
        todo_from_db = session.get(Todo, id)
        if todo_from_db is None:
            return {"error": "Todo not found"}
        else:
            session.delete(todo_from_db)
            session.commit()
            return {f"Todo with id {id} deleted successfully"}
        
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}