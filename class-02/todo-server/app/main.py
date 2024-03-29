from fastapi import FastAPI
todo_server: FastAPI = FastAPI()
Database_URL = "postgresql://online-todo-server_owner:bh1YJxmpDf5j@ep-winter-salad-a5wxh9rl.us-east-2.aws.neon.tech/online-todo-server?sslmode=require"
@todo_server.get('/')
def hello():
    return "Hello World"
