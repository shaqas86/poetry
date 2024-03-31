from http import client
from fastapi.testclient import TestClient
from sqlmodel import Session, select, create_engine,SQLModel,Field
from todo_server.main import engine
import pytest

from todo_server.main import app,get_session, Todo
from todo_server import settings


def test_read_main():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_write_main():
   
   connection_string=str(settings.TEST_DATABASE_URL).replace(
       "postgresql", "postgresql+psycopg"
   )
   engine=create_engine(connection_string)

   SQLModel.metadata.create_all(engine)
   print("creating table ...")
#     with Session(engine) as session:
#       t1 = Todo(title="todo1", description="desc1")
#       t2 = Todo(title="todo2", description="desc2")
#       session.add(t1)
#       session.add(t2)
#       session.commit()
     
    
   
# engine=create_engine(connection_string)
# SQLModel.metadata.create_all(engine)
# with Session(engine) as session:
       
#        def get_session_override():
#            return session
       
#        app.dependency_overrides[get_session] = get_session_override
#        client = TestClient(app=app)

#        todo_content = {"content": "test"}   
#        response = client.post("/todo/",json=todo_content)

#        data=response.json()
#        assert response.status_code == 200
#        assert data["content"] == todo_content

# def test_read_todos():
#     connection_string=str(settings.TEST_DATABASE_URL).replace(
#        "postgresql", "postgresql+psycopg"
#    )

#     SQLModel.metadata.create_all(create_engine(connection_string))
#     with Session(create_engine(connection_string)) as session:

#         def get_session_override():
#             return session

#         app.dependency_overrides[get_session] = get_session_override
#         client = TestClient(app=app)

#         response = client.get("/todos/")

#         assert response.status_code == 200
        
