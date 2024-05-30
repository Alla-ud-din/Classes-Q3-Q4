from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Field, create_engine, Session, select
from todo_app import setting
from todo_app.db import create_tables, get_session
from todo_app.router import user
from typing import Annotated
from contextlib import asynccontextmanager
from todo_app.auth import EXPIRY_TIME, authenticate_user, create_access_token, create_refresh_token, current_user, validate_refresh_token
from todo_app.models import Todo, Todo_Create, Todo_Edit, Token, User

# Step-1: Create Database on Neon
# Step-2: Create .env file for environment variables
# Step-3: Create setting.py file for encrypting DatabaseURL
# Step-4: Create a Model
# Step-5: Create Engine
# Step-6: Create function for table creation
# Step-7: Create function for session management
# Step-8: Create contex manager for app lifespan
# Step-9: Create all endpoints of todo app


# class Todo (SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     content: str = Field(index=True, min_length=3, max_length=54)
#     is_completed: bool = Field(default=False)


# engine is one for whole application
# connection_string: str = str(setting.DATABASE_URL).replace(
#     "postgresql", "postgresql+psycopg")
# engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300, pool_size=10, echo=True)


# def create_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Creating Tables')
    create_tables()
    print("Tables Created")
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan, title="dailyDo Todo App", version='1.0.0')

app.include_router(router=user.user_router)
@app.get('/')
async def root():
    return {"message": "Welcome to dailyDo todo app"}

#login . username, password

@app.post('/token', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)]):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=401, detail= "Invalid username or password")
    expiry_time = timedelta(minutes= EXPIRY_TIME)
    access_token = create_access_token({"sub":form_data.username}, expiry_time)

    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub":user.email}, refresh_expire_time)

    return Token(access_token = access_token, token_type = "bearer", refresh_token= refresh_token)

@app.post('/token/refresh')
def refresh_token(old_refresh_token:str,session:Annotated[Session, Depends(get_session)]):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"}
    )
    user = validate_refresh_token(old_refresh_token, session)
    if not user:
        raise credential_exception
    
    expiry_time = timedelta(minutes= EXPIRY_TIME)
    access_token = create_access_token({"sub":user.username}, expiry_time)

    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub":user.email}, refresh_expire_time)
    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)

@app.post('/todos/', response_model=Todo)
async def create_todo(current_user:Annotated[User, Depends(current_user)],todo: Todo_Create, session: Annotated[Session, Depends(get_session)]):
    new_todo = Todo(content=todo.content, user_id=current_user.id)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo


@app.get('/todos/', response_model=list[Todo])
async def get_all(current_user:Annotated[User, Depends(current_user)],session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    if todos:
        return todos
    else:
        raise HTTPException(status_code=404, detail="No Task found")


@app.get('/todos/{id}', response_model=Todo)
async def get_single_todo(id: int,current_user:Annotated[User, Depends(current_user)], session: Annotated[Session, Depends(get_session)]):

    user_todos = session.exec(select(Todo).where(Todo.id == id)).all()
    matched_todo = next((todo for todo in user_todos if todo.id == id), None)
    if matched_todo:
        return matched_todo
    else:
        raise HTTPException(status_code=404, detail="No Task found")


@app.put('/todos/{id}')
async def edit_todo(id: int, todo: Todo_Edit,current_user:Annotated[User, Depends(current_user)], session: Annotated[Session, Depends(get_session)]):
    user_todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    existing_todo = next((todo for todo in user_todos if todo.id == id), None)
    if existing_todo:
        existing_todo.content = todo.content
        existing_todo.is_completed = todo.is_completed
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException(status_code=404, detail="No task found")


@app.delete('/todos/{id}')
async def delete_todo(id: int, current_user:Annotated[User, Depends(current_user)], session: Annotated[Session, Depends(get_session)]): 
    user_todos = session.exec(select(Todo).where(Todo.id == id)).all()
    matched_todo = next((todo for todo in user_todos if todo.id == id), None)
    # todo = session.exec(select(Todo).where(Todo.id == id)).first()
    # todo = session.get(Todo,id)
    if matched_todo:
        session.delete(matched_todo)
        session.commit()
        # session.refresh(todo)
        return {"message": "Task successfully deleted"}
    else:
        raise HTTPException(status_code=404, detail="No task found")
    


# def greeter(name):
#     print("1. In Greeter Function")
#     greeting = name + " ,Welcome to Class"
#     return greeting

# 1
# @app.get('/')
# def hello(name: str):
#     print("2. In Hello Function")
#     greet_msg = greeter(name)
#     return {"greeting": greet_msg}

# 2
# @app.get('/')
# def hello(name: str, greet_msg = Depends(greeter)):
#     print("2. In Hello Function")
#     return {"greeting": greet_msg}

# 3
# @app.get('/')
# def hello(name: str, greet_msg: Annotated[str, Depends(greeter)]):     # str is the return type of greet_msg from greeter function
#     print("2. In Hello Function")
#     return {"greeting": greet_msg}