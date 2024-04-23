from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session
from contextlib import asynccontextmanager

from app import settings

# Step 1: Database Table SCHEMA
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    # primary_key=True specifies that this field is the primary key of the table. A primary key uniquely identifies each row in a database table.
    title: str
    description: str


# Connection to the database
conn_str: str = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)
# 1. Dialect: postgresql: This part specifies the type of database you're connecting to, which is PostgreSQL in this case.
# 2. Connector: psycopg: This part specifies the Python library that will be used to communicate with the PostgreSQL database. In this case, it's psycopg.
engine = create_engine(conn_str)
# create_engine to establish a connection to your database using the provided connection string.

def create_db_tables():
    print("create_db_tables")
    SQLModel.metadata.create_all(engine)
    # MetaData object associated with the SQLModel class acts as a registry that keeps track of all the database model classes 
    # create_all method iterates through all the model classes registered in the SQLModel.metadata object.
    print("done")

@asynccontextmanager
async def lifespan(todo_server: FastAPI):
    print("Server Startup")
    create_db_tables()
    yield

# Table Data Save, Get

todo_server: FastAPI = FastAPI(lifespan=lifespan)


@todo_server.post("/todo")
def create_todo(try_content: Todo):
        session = Session(engine)
        session.add(try_content)
        session.commit()
        session.refresh(try_content)
        session.close()
        return try_content